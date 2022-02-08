"""
Several tests for utils
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import math
import pytest
import s2sphere  # type: ignore

from gpxtrackposter.utils import (
    compute_grid,
    interpolate_color,
    format_float,
    make_key_times,
    compute_bounds_xy,
    lng2x,
    lat2y,
    latlng2xy,
)
from gpxtrackposter.value_range import ValueRange
from gpxtrackposter.xy import XY


@pytest.mark.parametrize(
    "test_value, expected_result",
    [
        (s2sphere.LatLng.from_degrees(47.998933, 7.841819), XY(1.043565661111111, 0.1952376901623566)),
        (s2sphere.LatLng.from_degrees(40.711344, -74.005382), XY(0.5888589888888889, 0.2519722679166857)),
    ],
)
def test_latlng2xy(test_value: s2sphere.LatLng, expected_result: XY) -> None:
    assert math.isclose(expected_result.x, latlng2xy(test_value).x, rel_tol=0.000001)
    assert math.isclose(expected_result.y, latlng2xy(test_value).y, rel_tol=0.000001)


@pytest.mark.parametrize(
    "test_value, expected_result",
    [
        (-180, 0.0),
        (-120, 1 / 3),
        (-90, 1 / 2),
        (-60, 2 / 3),
        (-30, 5 / 6),
        (0, 1.0),
        (30, 7 / 6),
        (60, 4 / 3),
        (90, 3 / 2),
        (120, 5 / 3),
        (180, 2.0),
    ],
)
def test_lng2x(test_value: int, expected_result: float) -> None:
    assert math.isclose(expected_result, lng2x(test_value), rel_tol=0.000001)


@pytest.mark.parametrize(
    "test_value, expected_result",
    [
        (-60, 0.9192007182789828),
        (-30, 0.6748495762830298),
        (0, 0.5),
        (30, 0.3251504237169702),
        (60, 0.08079928172101752),
    ],
)
def test_lat2y(test_value: int, expected_result: float) -> None:
    math.isclose(expected_result, lat2y(test_value), rel_tol=0.000001)


@pytest.mark.parametrize(
    "test_value, expected_result",
    [
        (
            [[XY(1, 1), XY(2, 4)], [XY(3, 9), XY(-4, -16)]],
            (ValueRange.from_pair(-4, 3), ValueRange.from_pair(-16, 9)),
        ),
        (
            [[XY(1, 1), XY(-2, -4)], [XY(3, 9), XY(4, 16)]],
            (ValueRange.from_pair(-2, 4), ValueRange.from_pair(-4, 16)),
        ),
    ],
)
def test_compute_bounds_xy(test_value: list, expected_result: tuple) -> None:
    bounds_xy = compute_bounds_xy(test_value)
    assert expected_result[0].lower() == bounds_xy[0].lower()
    assert expected_result[0].upper() == bounds_xy[0].upper()
    assert expected_result[1].lower() == bounds_xy[1].lower()
    assert expected_result[1].upper() == bounds_xy[1].upper()


@pytest.mark.parametrize(
    "count, dimensions, expected_best_size, expected_best_counts",
    [
        (1, XY(1, 1), 1.0, (1, 1)),
        (2, XY(1, 1), 0.5, (1, 2)),
        (3, XY(1, 1), 0.5, (2, 2)),
        (4, XY(1, 1), 0.5, (2, 2)),
        (10, XY(1, 1), 0.25, (3, 4)),
        (99, XY(1, 1), 0.1, (10, 10)),
    ],
)
def test_compute_grid(count: int, dimensions: XY, expected_best_size: float, expected_best_counts: tuple) -> None:
    assert (expected_best_size, expected_best_counts) == compute_grid(count, dimensions)


@pytest.mark.parametrize(
    "color1, color2, ratio, expected_color",
    [
        ("#000000", "#ffffff", 0, "#000000"),
        ("#000000", "#ffffff", 1, "#ffffff"),
        ("#000000", "#ffffff", 0.5, "#7f7f7f"),
        ("#000000", "#ffffff", -100, "#000000"),
        ("#000000", "#ffffff", 12345, "#ffffff"),
    ],
)
def test_interpolate_color(color1: str, color2: str, ratio: float, expected_color: str) -> None:
    assert expected_color == interpolate_color(color1, color2, ratio)


@pytest.mark.parametrize(
    "test_value, expected_result",
    [
        (1, "1.0"),
        (0.12, "0.1"),
        (0.56, "0.6"),
    ],
)
def test_format_float(test_value: float, expected_result: str) -> None:
    assert expected_result == format_float(test_value)
    assert math.isclose(float(expected_result), float(format_float(test_value)), rel_tol=0.000001)


@pytest.mark.parametrize(
    "test_value, expected_result",
    [
        (1, ["0", "1"]),
        (5, ["0", "0.2", "0.4", "0.6", "0.8", "1"]),
        (10, ["0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0", "1"]),
    ],
)
def test_make_key_times(test_value: int, expected_result: list) -> None:
    assert expected_result == make_key_times(test_value)
