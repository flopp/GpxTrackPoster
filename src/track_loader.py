# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import hashlib
import os
import shutil
import typing
import concurrent.futures
from . import track
from . import year_range


def load_gpx_file(file_name: str) -> track.Track:
    print("Loading track {}...".format(os.path.basename(file_name)))
    t = track.Track()
    t.load_gpx(file_name)
    return t


def load_cached_track_file(file_name: str, cache_dir: str) -> track.Track:
    checksum = hashlib.sha256(open(file_name, 'rb').read()).hexdigest()
    cache_file = os.path.join(cache_dir, checksum + ".json")
    t = track.Track()
    t.load_cache(cache_file)
    t.file_names = [os.path.basename(file_name)]
    return t


class TrackLoader:
    def __init__(self):
        self.min_length = 1000
        self.special_file_names = []
        self.year_range = year_range.YearRange()
        self.cache_dir = None

    def clear_cache(self):
        if os.path.isdir(self.cache_dir):
            print("Removing cache dir: {}".format(self.cache_dir))
            try:
                shutil.rmtree(self.cache_dir)
            except OSError as e:
                print("Failed: {}".format(e))

    def load_tracks(self, base_dir: str) -> typing.List[track.Track]:
        file_names = [x for x in self.__list_gpx_files(base_dir)]
        print("GPX files: {}".format(len(file_names)))

        tracks = []

        # load track from cache
        cached_tracks = []
        if self.cache_dir:
            print("Trying to load {} track(s) from cache...".format(len(file_names)))
            cached_tracks = self.__load_tracks_from_cache(file_names, self.cache_dir)
            print("Loaded tracks from cache:", len(cached_tracks))
            tracks = list(cached_tracks.values())

        # load remaining gpx files
        remaining_file_names = [f for f in file_names if f not in cached_tracks]
        if remaining_file_names:
            print("Trying to load {} track(s) from GPX files; this may take a while..."
                  .format(len(remaining_file_names)))
            loaded_tracks = self.__load_tracks(remaining_file_names)
            print("Conventionally loaded tracks:", len(loaded_tracks))

            # store non-cached tracks in cache
            if loaded_tracks and self.cache_dir:
                print("Storing {} track(s) in cache...".format(len(loaded_tracks)))
                for (file_name, t) in loaded_tracks.items():
                    checksum = hashlib.sha256(open(file_name, 'rb').read()).hexdigest()
                    cache_file = os.path.join(self.cache_dir, checksum + ".json")
                    t.store_cache(cache_file)
            tracks.extend(loaded_tracks.values())

        tracks = self.__filter_tracks(tracks)

        # merge tracks that took place within one hour
        tracks = self.__merge_tracks(tracks)

        # filter out tracks with length < min_length
        return [t for t in tracks if t.length >= self.min_length]

    def __filter_tracks(self, tracks: typing.List[track.Track]) -> typing.List[track.Track]:
        filtered_tracks = []
        for t in tracks:
            file_name = t.file_names[0]
            if t.length == 0:
                print("{}: skipping empty track".format(file_name))
            elif not t.start_time:
                print("{}: skipping track without start time".format(file_name))
            elif not self.year_range.contains(t.start_time):
                print("{}: skipping track with wrong year {}".format(file_name, t.start_time.year))
            else:
                t.special = (file_name in self.special_file_names)
                filtered_tracks.append(t)
        return filtered_tracks

    @staticmethod
    def __merge_tracks(tracks: typing.List[track.Track]) -> typing.List[track.Track]:
        print("Merging tracks...")
        tracks = sorted(tracks, key=lambda t1: t1.start_time)
        merged_tracks = []
        last_end_time = None
        for t in tracks:
            if last_end_time is None:
                merged_tracks.append(t)
            else:
                dt = (t.start_time - last_end_time).total_seconds()
                if 0 < dt < 3600:
                    merged_tracks[-1].append(t)
                else:
                    merged_tracks.append(t)
            last_end_time = t.end_time
        print("Merged {} track(s)".format(len(tracks) - len(merged_tracks)))
        return merged_tracks

    @staticmethod
    def __load_tracks(file_names: typing.List[str]) -> typing.List[track.Track]:
        tracks = {}
        with concurrent.futures.ProcessPoolExecutor() as executor:
            future_to_file_name = {
                executor.submit(load_gpx_file, file_name): file_name for file_name in file_names
            }
        for future in concurrent.futures.as_completed(future_to_file_name):
            file_name = future_to_file_name[future]
            try:
                t = future.result()
            except Exception as e:
                print("Error while loading {}: {}".format(file_name, e))
            else:
                tracks[file_name] = t

        return tracks

    @staticmethod
    def __load_tracks_from_cache(file_names: typing.List[str], cache_dir: str) -> typing.List[track.Track]:
        tracks = {}
        failed_loads = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            future_to_file_name = {
                executor.submit(load_cached_track_file, file_name, cache_dir): file_name for file_name in file_names
            }
        for future in concurrent.futures.as_completed(future_to_file_name):
            file_name = future_to_file_name[future]
            try:
                t = future.result()
            except Exception as e:
                failed_loads.append((file_name, e))
            else:
                tracks[file_name] = t
        return tracks

    @staticmethod
    def __list_gpx_files(base_dir: str) -> typing.Generator[str, None, None]:
        base_dir = os.path.abspath(base_dir)
        if not os.path.isdir(base_dir):
            raise Exception("Not a directory: {}".format(base_dir))
        for name in os.listdir(base_dir):
            path_name = os.path.join(base_dir, name)
            if name.endswith(".gpx") and os.path.isfile(path_name):
                yield path_name
