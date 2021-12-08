"""
Several tests for utils
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import unittest

import s2sphere  # type: ignore

from gpxtrackposter.utils import (
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


class TestCase(unittest.TestCase):
    """
    Test class for utils
    """

    def setUp(self) -> None:
        self.maxDiff = 5000

    def test_latlng2xy(self) -> None:
        test_values = [
            (s2sphere.LatLng.from_degrees(47.998933, 7.841819), XY(1.043565661111111, 0.1952376901623566)),
            (s2sphere.LatLng.from_degrees(40.711344, -74.005382), XY(0.5888589888888889, 0.2519722679166857)),
        ]
        for test_value, expected_result in test_values:
            with self.subTest(f"{test_value} -> {expected_result}"):
                self.assertAlmostEqual(expected_result.x, latlng2xy(test_value).x, 12)
                self.assertAlmostEqual(expected_result.y, latlng2xy(test_value).y, 12)

    def test_lng2x(self) -> None:
        test_values = [
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
        ]
        for test_value, expected_result in test_values:
            with self.subTest(f"{test_value} -> {expected_result}"):
                self.assertAlmostEqual(expected_result, lng2x(test_value), 12)

    def test_lat2y(self) -> None:
        test_values = [
            (-60, 0.9192007182789828),
            (-30, 0.6748495762830298),
            (0, 0.5),
            (30, 0.3251504237169702),
            (60, 0.08079928172101752),
        ]
        for test_value, expected_result in test_values:
            with self.subTest(f"{test_value} -> {expected_result}"):
                self.assertAlmostEqual(expected_result, lat2y(test_value), 12)

    def test_compute_bounds_xy(self) -> None:
        test_values = [
            (
                [[XY(1, 1), XY(2, 4)], [XY(3, 9), XY(-4, -16)]],
                (ValueRange.from_pair(-4, 3), ValueRange.from_pair(-16, 9)),
            ),
            (
                [[XY(1, 1), XY(-2, -4)], [XY(3, 9), XY(4, 16)]],
                (ValueRange.from_pair(-2, 4), ValueRange.from_pair(-4, 16)),
            ),
        ]
        for test_value, expected_result in test_values:
            with self.subTest(f"{test_value} -> {expected_result}"):
                bounds_xy = compute_bounds_xy(test_value)
                self.assertEqual(expected_result[0].lower(), bounds_xy[0].lower())
                self.assertEqual(expected_result[0].upper(), bounds_xy[0].upper())
                self.assertEqual(expected_result[1].lower(), bounds_xy[1].lower())
                self.assertEqual(expected_result[1].upper(), bounds_xy[1].upper())

    def test_interpolate_color(self) -> None:
        self.assertEqual("#000000", interpolate_color("#000000", "#ffffff", 0))
        self.assertEqual("#ffffff", interpolate_color("#000000", "#ffffff", 1))
        self.assertEqual("#7f7f7f", interpolate_color("#000000", "#ffffff", 0.5))
        self.assertEqual("#000000", interpolate_color("#000000", "#ffffff", -100))
        self.assertEqual("#ffffff", interpolate_color("#000000", "#ffffff", 12345))

    def test_format_float(self) -> None:
        test_values = [
            (1, "1.0"),
            (0.12, "0.1"),
            (0.56, "0.6"),
        ]
        for test_value, expected_result in test_values:
            with self.subTest(f"{test_value} -> {expected_result}"):
                self.assertEqual(expected_result, format_float(test_value))
                self.assertAlmostEqual(float(expected_result), float(format_float(test_value)), 1)

    def test_make_key_times(self) -> None:
        test_values = [
            (1, ["0", "1"]),
            (5, ["0", "0.2", "0.4", "0.6", "0.8", "1"]),
            (10, ["0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0", "1"]),
        ]
        for test_value, expected_result in test_values:
            with self.subTest(f"{test_value} -> {expected_result}"):
                self.assertListEqual(expected_result, make_key_times(test_value))


if __name__ == "__main__":
    unittest.main()
