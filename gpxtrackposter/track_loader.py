"""Handle parsing of GPX files and writing/loading of cached data"""


# Copyright 2016-2023 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import concurrent.futures
import hashlib
import logging
import os
import json
import datetime
import shutil
import typing
from typing import Any

import pint  # type: ignore
import s2sphere  # type: ignore
from stravalib import Client  # type: ignore

from gpxtrackposter.exceptions import ParameterError, TrackLoadError
from gpxtrackposter.timezone_adjuster import TimezoneAdjuster
from gpxtrackposter.track import Track
from gpxtrackposter.units import Units
from gpxtrackposter.year_range import YearRange

log = logging.getLogger(__name__)


def load_gpx_file(file_name: str, timezone_adjuster: TimezoneAdjuster) -> Track:
    """Load an individual GPX file as a track by using Track.load_gpx()"""
    log.info("Loading track %s...", os.path.basename(file_name))
    t = Track()
    t.load_gpx(file_name, timezone_adjuster)
    return t


def load_cached_track_file(cache_file_name: str, file_name: str) -> Track:
    """Load an individual track from cache files"""
    try:
        t = Track()
        t.load_cache(cache_file_name)
        t.file_names = [os.path.basename(file_name)]
        log.info("Loaded track %s from cache file %s", file_name, cache_file_name)
        return t
    except Exception as e:
        raise TrackLoadError("Failed to load track from cache.") from e


class TrackLoader:
    """Handle the loading of tracks from cache and/or GPX files

    Attributes:
        _min_length: All tracks shorter than this value are filtered out.
        special_file_names: Tracks marked as special in command line args
        year_range: All tracks outside of this range will be filtered out.
        cache_dir: Directory used to store cached tracks
        _activity_type: Only gpx files with activity type are considered

    Methods:
        clear_cache: Remove cache directory
        load_tracks: Load all data from cache and GPX files
    """

    def __init__(self, workers: typing.Optional[int]) -> None:
        self._workers = workers
        self._min_length: pint.Quantity = 1 * Units().km
        self.special_file_names: typing.List[str] = []
        self.year_range = YearRange()
        self.cache_dir: typing.Optional[str] = None
        self.strava_cache_file = ""
        self._cache_file_names: typing.Dict[str, str] = {}
        self._activity_type: str = "all"

    def set_cache_dir(self, cache_dir: str) -> None:
        self.cache_dir = cache_dir

    def clear_cache(self) -> None:
        """Remove cache directory, if it exists"""
        if self.cache_dir is not None and os.path.isdir(self.cache_dir):
            log.info("Removing cache dir: %s", self.cache_dir)
            try:
                shutil.rmtree(self.cache_dir)
            except OSError as e:
                log.error("Failed: %s", str(e))

    def set_min_length(self, min_length: pint.Quantity) -> None:
        self._min_length = min_length

    def set_activity(self, activity_type: str) -> None:
        self._activity_type = activity_type.lower()

    def load_tracks(self, base_dir: str) -> typing.List[Track]:
        """Load tracks base_dir and return as a List of tracks"""
        file_names = list(self._list_gpx_files(base_dir))
        log.info("GPX files: %d", len(file_names))

        tracks: typing.List[Track] = []

        # load track from cache
        cached_tracks: typing.Dict[str, Track] = {}
        if self.cache_dir:
            log.info("Trying to load %d track(s) from cache...", len(file_names))
            cached_tracks = self._load_tracks_from_cache(file_names)
            log.info("Loaded tracks from cache: %d", len(cached_tracks))
            tracks = list(cached_tracks.values())

        # load remaining gpx files
        remaining_file_names = [f for f in file_names if f not in cached_tracks]
        if remaining_file_names:
            log.info("Trying to load %d track(s) from GPX files; this may take a while...", len(remaining_file_names))
            timezone_adjuster = TimezoneAdjuster()
            loaded_tracks = self._load_tracks(remaining_file_names, timezone_adjuster)
            tracks.extend(loaded_tracks.values())
            log.info("Conventionally loaded tracks: %d", len(loaded_tracks))
            self._store_tracks_to_cache(loaded_tracks)

        return self._filter_and_merge_tracks(tracks)

    def load_strava_tracks(self, strava_config: str) -> typing.List[Track]:
        tracks = []
        tracks_names = []
        if self.cache_dir:
            self.strava_cache_file = os.path.join(self.cache_dir, strava_config)
            if os.path.isfile(self.strava_cache_file):
                with open(self.strava_cache_file, encoding="utf8") as f:
                    strava_cache_data = json.load(f)
                    tracks = [self._strava_cache_to_track(i) for i in strava_cache_data]
                    tracks_names = [track.file_names[0] for track in tracks]

        with open(strava_config, encoding="utf8") as f:
            strava_data = json.load(f)
        filter_type = strava_data.pop("activity_type", None)
        client = Client()
        response = client.refresh_access_token(**strava_data)
        client.access_token = response["access_token"]
        filter_dict = {"before": datetime.datetime.utcnow()}
        if tracks:
            max_time = max(track.start_time() for track in tracks)
            filter_dict = {"after": max_time - datetime.timedelta(days=2)}
        for activity in client.get_activities(**filter_dict):
            # tricky to pass the timezone
            if str(activity.id) in tracks_names:
                continue
            if filter_type and activity.type not in (
                [filter_type] if isinstance(filter_type, str) else filter_type
            ):  # pylint: disable=superfluous-parens
                continue
            t = Track()
            t.load_strava(activity)
            tracks.append(t)
        self._store_strava_tracks_to_cache(tracks)
        return self._filter_and_merge_tracks(tracks)

    def _filter_tracks(self, tracks: typing.List[Track]) -> typing.List[Track]:
        filtered_tracks = []
        for t in tracks:
            file_name = t.file_names[0]
            if t.length().magnitude == 0:
                log.info("%s: skipping empty track", file_name)
            elif not t.has_time():
                log.info("%s: skipping track without start or end time", file_name)
            elif not self.year_range.contains(t.start_time()):
                log.info("%s: skipping track with wrong year %d", file_name, t.start_time().year)
            else:
                t.special = file_name in self.special_file_names
                filtered_tracks.append(t)
        return filtered_tracks

    def _filter_and_merge_tracks(self, tracks: typing.List[Track]) -> typing.List[Track]:
        tracks = self._filter_tracks(tracks)
        # merge tracks that took place within one hour
        tracks = self._merge_tracks(tracks)
        # filter out tracks with length < min_length
        tracks = [t for t in tracks if t.length() >= self._min_length]
        # filter out tracks with wrong activity type
        tracks = [t for t in tracks if self._activity_type in (t.activity_type, "all")]
        return tracks

    @staticmethod
    def _merge_tracks(tracks: typing.List[Track]) -> typing.List[Track]:
        log.info("Merging tracks...")
        tracks = sorted(tracks, key=lambda t1: t1.start_time())
        merged_tracks = []
        last_end_time = None
        for t in tracks:
            if last_end_time is None:
                merged_tracks.append(t)
            else:
                dt = (t.start_time() - last_end_time).total_seconds()
                if 0 < dt < 3600:
                    merged_tracks[-1].append(t)
                else:
                    merged_tracks.append(t)
            last_end_time = t.end_time()
        log.info("Merged %d track(s)", len(tracks) - len(merged_tracks))
        return merged_tracks

    def _load_tracks(
        self, file_names: typing.List[str], timezone_adjuster: TimezoneAdjuster
    ) -> typing.Dict[str, Track]:
        tracks = {}

        if self._workers is not None and self._workers <= 1:
            for file_name in file_names:
                try:
                    t = load_gpx_file(file_name, timezone_adjuster)
                except TrackLoadError as e:
                    log.error("Error while loading %s: %s", file_name, str(e))
                else:
                    tracks[file_name] = t
            return tracks

        with concurrent.futures.ProcessPoolExecutor(max_workers=self._workers) as executor:
            future_to_file_name = {
                executor.submit(load_gpx_file, file_name, timezone_adjuster): file_name for file_name in file_names
            }
        for future in concurrent.futures.as_completed(future_to_file_name):
            file_name = future_to_file_name[future]
            try:
                t = future.result()
            except TrackLoadError as e:
                log.error("Error while loading %s: %s", file_name, str(e))
            else:
                tracks[file_name] = t

        return tracks

    def _load_tracks_from_cache(self, file_names: typing.List[str]) -> typing.Dict[str, Track]:
        tracks = {}

        if self._workers is not None and self._workers <= 1:
            for file_name in file_names:
                try:
                    t = load_cached_track_file(self._get_cache_file_name(file_name), file_name)
                except Exception:
                    # silently ignore failed cache load attempts
                    pass
                else:
                    tracks[file_name] = t
            return tracks

        with concurrent.futures.ProcessPoolExecutor(max_workers=self._workers) as executor:
            future_to_file_name = {
                executor.submit(load_cached_track_file, self._get_cache_file_name(file_name), file_name): file_name
                for file_name in file_names
            }
        for future in concurrent.futures.as_completed(future_to_file_name):
            file_name = future_to_file_name[future]
            try:
                t = future.result()
            except Exception:
                # silently ignore failed cache load attempts
                pass
            else:
                tracks[file_name] = t

        return tracks

    def _store_tracks_to_cache(self, tracks: typing.Dict[str, Track]) -> None:
        if (not tracks) or (not self.cache_dir):
            return

        log.info("Storing %d track(s) to cache...", len(tracks))
        for file_name, t in tracks.items():
            try:
                t.store_cache(self._get_cache_file_name(file_name))
            except Exception as e:
                log.error("Failed to store track %s to cache: %s", file_name, str(e))
            else:
                log.info("Stored track %s to cache", file_name)

    def _store_strava_tracks_to_cache(self, tracks: typing.List[Track]) -> None:
        if (not tracks) or (not self.cache_dir):
            return
        dirname = os.path.dirname(self.strava_cache_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        log.info("Storing %d track(s) to cache...", len(tracks))
        to_cache_tracks = [self._make_strava_cache_dict(track) for track in tracks]
        with open(self.strava_cache_file, "w", encoding="utf8") as f:
            json.dump(to_cache_tracks, f)

    @staticmethod
    def _make_strava_cache_dict(track: Track) -> typing.Dict[str, Any]:
        lines_data = []
        for line in track.polylines:
            lines_data.append([{"lat": latlng.lat().degrees, "lng": latlng.lng().degrees} for latlng in line])
        return {
            "name": track.file_names[0],  # strava id
            "start": track.start_time().strftime("%Y-%m-%d %H:%M:%S"),
            "end": track.end_time().strftime("%Y-%m-%d %H:%M:%S"),
            "length": track.length_meters,
            "segments": lines_data,
        }

    @staticmethod
    def _strava_cache_to_track(data: typing.Dict[str, Any]) -> "Track":
        t = Track()
        t.file_names = [data["name"]]
        t.set_start_time(datetime.datetime.strptime(data["start"], "%Y-%m-%d %H:%M:%S"))
        t.set_end_time(datetime.datetime.strptime(data["end"], "%Y-%m-%d %H:%M:%S"))
        t.length_meters = float(data["length"])
        t.polylines = []
        for data_line in data["segments"]:
            t.polylines.append([s2sphere.LatLng.from_degrees(float(d["lat"]), float(d["lng"])) for d in data_line])
        return t

    @staticmethod
    def _list_gpx_files(base_dir: str) -> typing.Generator[str, None, None]:
        base_dir = os.path.abspath(base_dir)
        if not os.path.isdir(base_dir):
            raise ParameterError(f"Not a directory: {base_dir}")
        for name in os.listdir(base_dir):
            path_name = os.path.join(base_dir, name)
            if name.endswith(".gpx") and os.path.isfile(path_name):
                yield path_name

    def _get_cache_file_name(self, file_name: str) -> str:
        assert self.cache_dir

        if file_name in self._cache_file_names:
            return self._cache_file_names[file_name]

        try:
            with open(file_name, "rb") as file:
                checksum = hashlib.sha256(file.read()).hexdigest()
        except PermissionError as e:
            raise TrackLoadError("Failed to compute checksum (bad permissions).") from e
        except Exception as e:
            raise TrackLoadError("Failed to compute checksum.") from e

        cache_file_name = os.path.join(self.cache_dir, f"{checksum}.json")
        self._cache_file_names[file_name] = cache_file_name
        return cache_file_name
