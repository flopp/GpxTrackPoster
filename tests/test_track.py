"""
Several tests for Track
"""
# Copyright 2022-2023 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import datetime
import os
import re

import pytest
import s2sphere  # type: ignore
from pint import Quantity  # type: ignore

from gpxtrackposter.exceptions import TrackLoadError
from gpxtrackposter.track import Track
from gpxtrackposter.units import Units


def test_init() -> None:
    track = Track()
    assert len(track.file_names) == 0
    assert len(track.polylines) == 0
    assert not track.special
    assert not track.activity_type
    assert not track.has_time()
    assert 0.0 == track.length_meters
    assert 0.0 * Units().meter == track.length()


def test_set_start_time() -> None:
    track = Track()
    start_time = datetime.datetime(2022, 1, 1, 1, 1, 1)
    track.set_start_time(start_time)
    assert start_time == track.start_time()
    assert not track.has_time()


def test_set_end_time() -> None:
    track = Track()
    end_time = datetime.datetime(2022, 2, 2, 2, 2, 2)
    track.set_end_time(end_time)
    assert end_time == track.end_time()
    assert not track.has_time()


def test_set_start_and_end_time() -> None:
    track = Track()
    start_time = datetime.datetime(2022, 1, 1, 1, 1, 1)
    end_time = datetime.datetime(2022, 2, 2, 2, 2, 2)
    assert not track.has_time()
    track.set_start_time(start_time)
    track.set_end_time(end_time)
    assert track.has_time()


def test_length_meters() -> None:
    track = Track()
    assert 0.0 == track.length_meters
    track.length_meters = 1234.5
    assert 1234.5 == track.length_meters
    assert Quantity(1234.5, "meter") == track.length()


def test_load_gpx_file_does_not_exist() -> None:
    track = Track()
    with pytest.raises(TrackLoadError, match=re.escape("Something went wrong when loading GPX.")):
        test_dir = "this_dir_does_not_exist/this_file_does_not_exist.gpx"
        assert not os.path.isdir(test_dir)
        track.load_gpx(test_dir, None)


def test_load_gpx_empty_file(gpx_file_empty: str) -> None:
    track = Track()
    with pytest.raises(TrackLoadError, match="Empty GPX file"):
        track.load_gpx(gpx_file_empty, None)


def test_load_gpx_invalid_file(gpx_file_invalid: str) -> None:
    track = Track()
    with pytest.raises(TrackLoadError, match=re.escape("Failed to parse GPX.")):
        track.load_gpx(gpx_file_invalid, None)


def test_load_gpx_no_permission(gpx_file_no_permission: str) -> None:
    track = Track()
    with pytest.raises(TrackLoadError, match=re.escape("Cannot load GPX (bad permissions)")):
        track.load_gpx(gpx_file_no_permission, None)


def test_load_gpx_no_length(gpx_file_track_no_length: str) -> None:
    track = Track()
    with pytest.raises(TrackLoadError, match=re.escape("Track is empty.")):
        track.load_gpx(gpx_file_track_no_length, None)


def test_load_gpx_valid_file_walk(gpx_file_track_walk: str) -> None:
    track = Track()
    assert len(track.polylines) == 0
    track.load_gpx(gpx_file_track_walk, None)
    assert len(track.polylines) != 0
    assert track.has_time()
    assert track.activity_type == "walk"


def test_load_gpx_valid_file_no_type(gpx_file_track_no_type: str) -> None:
    track = Track()
    assert len(track.polylines) == 0
    track.load_gpx(gpx_file_track_no_type, None)
    assert len(track.polylines) != 0
    assert track.has_time()
    assert not track.activity_type


def test_load_gpx_valid_file_append(gpx_file_track_walk: str, gpx_file_track_no_type: str) -> None:
    track = Track()
    track2 = Track()
    track.load_gpx(gpx_file_track_walk, None)
    length_before = track.length()
    track2.load_gpx(gpx_file_track_no_type, None)
    track.append(track2)
    assert track.length() > length_before


def test_bbox(gpx_file_track_walk: str) -> None:
    track = Track()
    track.load_gpx(gpx_file_track_walk, None)
    assert track.bbox() == s2sphere.sphere.LatLngRect.from_point_pair(
        s2sphere.LatLng.from_degrees(52.516495, 13.377094),
        s2sphere.LatLng.from_degrees(52.517959, 13.380634),
    )
