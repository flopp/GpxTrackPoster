# Copyright 2016-2018 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import datetime
import gpxpy as mod_gpxpy
import json
import os
import s2sphere as s2
from .exceptions import TrackLoadError


class Track:
    def __init__(self):
        self.file_names = []
        self.polylines = []
        self.start_time = None
        self.end_time = None
        self.length = 0
        self.special = False

    def load_gpx(self, file_name: str):
        try:
            self.file_names = [os.path.basename(file_name)]
            with open(file_name, 'r') as file:
                self._load_gpx_data(mod_gpxpy.parse(file))
        except TrackLoadError as e:
            raise e
        except mod_gpxpy.gpx.GPXXMLSyntaxException as e:
            raise TrackLoadError("Failed to parse GPX.") from e
        except PermissionError as e:
            raise TrackLoadError('Cannot load GPX (bad permissions)') from e
        except Exception as e:
            raise TrackLoadError("Something went wrong when loading GPX.") from e

    def bbox(self) -> s2.LatLngRect:
        bbox = s2.LatLngRect()
        for line in self.polylines:
            for latlng in line:
                bbox = bbox.union(s2.LatLngRect.from_point(latlng.normalized()))
        return bbox

    def _load_gpx_data(self, gpx: 'mod_gpxpy.gpx.GPX'):
        self.start_time, self.end_time = gpx.get_time_bounds()
        if self.start_time is None:
            raise TrackLoadError("Track has no start time.")
        if self.end_time is None:
            raise TrackLoadError("Track has no end time.")
        self.length = gpx.length_2d()
        if self.length == 0:
            raise TrackLoadError("Track is empty.")
        gpx.simplify()
        for t in gpx.tracks:
            for s in t.segments:
                line = [s2.LatLng.from_degrees(p.latitude, p.longitude) for p in s.points]
                self.polylines.append(line)

    def append(self, other: 'Track'):
        self.end_time = other.end_time
        self.polylines.extend(other.polylines)
        self.length += other.length
        self.file_names.extend(other.file_names)
        self.special = self.special or other.special

    def load_cache(self, cache_file_name: str):
        try:
            with open(cache_file_name) as data_file:
                data = json.load(data_file)
                self.start_time = datetime.datetime.strptime(data["start"], "%Y-%m-%d %H:%M:%S")
                self.end_time = datetime.datetime.strptime(data["end"], "%Y-%m-%d %H:%M:%S")
                self.length = float(data["length"])
                self.polylines = []
                for data_line in data["segments"]:
                    self.polylines.append([s2.LatLng.from_degrees(float(d["lat"]), float(d["lng"])) for d in data_line])
        except Exception as e:
            raise TrackLoadError('Failed to load track data from cache.') from e

    def store_cache(self, cache_file_name: str):
        dir_name = os.path.dirname(cache_file_name)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        with open(cache_file_name, 'w') as json_file:
            lines_data = []
            for line in self.polylines:
                lines_data.append([{"lat": latlng.lat().degrees, "lng": latlng.lng().degrees} for latlng in line])
            json.dump({"start": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                       "end": self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                       "length": self.length,
                       "segments": lines_data},
                      json_file)
