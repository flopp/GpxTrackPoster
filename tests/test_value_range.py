"""
Several tests for ValueRange
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import unittest

from gpxtrackposter.value_range import ValueRange


class TestCase(unittest.TestCase):
    """
    Test class for ValueRange
    """

    def test_init_returns_invalid_instance(self) -> None:
        """ValueRange object is initialised with None values, thus invalid"""
        value_range = ValueRange()
        self.assertFalse(value_range.is_valid())

    def test_from_pair_returns_instance(self) -> None:
        """from_pair returns instance of ValueRange"""
        value_range = ValueRange.from_pair(0.0, 0.0)
        self.assertTrue(value_range.is_valid())
        self.assertIsInstance(value_range, ValueRange)

    def test_clear_returns_invalid_empty_instance(self) -> None:
        float_pairs = [(0.0, 0.0), (0.0, 1.0), (-1.0, 0.0)]
        for float_1, float_2 in float_pairs:
            value_range = ValueRange.from_pair(float_1, float_2)
            self.assertTrue(value_range.is_valid())
            self.assertEqual(value_range.lower(), float_1)
            value_range.clear()
            self.assertFalse(value_range.is_valid())
            self.assertEqual(value_range.lower(), None)
            self.assertEqual(value_range.upper(), None)

    def test_lower_returns_lower_value(self) -> None:
        float_pairs = [
            (0.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (-1.0, 0.0, -1.0),
            (1.0, 0.0, 0.0),
            (0.0, -1.0, -1.0),
            (-1.0, 1.0, -1.0),
        ]
        for float_1, float_2, lower in float_pairs:
            value_range = ValueRange.from_pair(float_1, float_2)
            self.assertEqual(value_range.lower(), min(float_1, float_2))
            self.assertEqual(value_range.lower(), lower)

    def test_upper_returns_upper_value(self) -> None:
        float_pairs = [
            (0.0, 0.0, 0.0),
            (0.0, 1.0, 1.0),
            (-1.0, 0.0, 0.0),
            (1.0, 0.0, 1.0),
            (0.0, -1.0, 0.0),
            (-1.0, 1.0, 1.0),
        ]
        for float_1, float_2, upper in float_pairs:
            value_range = ValueRange.from_pair(float_1, float_2)
            self.assertEqual(value_range.upper(), max(float_1, float_2))
            self.assertEqual(value_range.upper(), upper)

    def test_diameter_returns_difference(self) -> None:
        float_pairs = [
            (0.0, 0.0, 0.0),
            (0.0, 1.0, 1.0),
            (-1.0, 0.0, 1.0),
            (1.0, 0.0, 1.0),
            (0.0, -1.0, 1.0),
            (-1.0, 1.0, 2.0),
        ]
        for float_1, float_2, difference in float_pairs:
            value_range = ValueRange.from_pair(float_1, float_2)
            self.assertEqual(value_range.diameter(), difference)

    def test_contains_returns_true(self) -> None:
        float_pairs = [
            (0.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (-1.0, 0.0, 0.0),
            (1.0, 0.0, 0.1),
            (0.0, -1.0, -0.5),
            (-1.0, 1.0, -1),
        ]
        for float_1, float_2, value in float_pairs:
            value_range = ValueRange.from_pair(float_1, float_2)
            self.assertTrue(value_range.contains(value))

    def test_contains_returns_false(self) -> None:
        float_pairs = [
            (0.0, 0.0, 1.0),
            (0.0, 1.0, 2.0),
            (-1.0, 0.0, 2.0),
            (1.0, 0.0, -1.0),
            (0.0, -1.0, 0.5),
            (-1.0, 1.0, -2),
        ]
        for float_1, float_2, value in float_pairs:
            value_range = ValueRange.from_pair(float_1, float_2)
            self.assertFalse(value_range.contains(value))

    def test_extend_with_invalid_instance_returns_valid(self) -> None:
        value = 1.0
        value_range = ValueRange()
        self.assertFalse(value_range.is_valid())
        value_range.extend(value)
        self.assertTrue(value_range.is_valid())
        self.assertEqual(value_range.lower(), value)
        self.assertEqual(value_range.upper(), value)

    def test_extend_returns_extended_value_range(self) -> None:
        float_pairs = [
            (0.0, 0.0, 1.0),
            (0.0, 1.0, 2.0),
            (-1.0, 0.0, 2.0),
            (1.0, 0.0, -1.0),
            (0.0, -1.0, 0.5),
            (-1.0, 1.0, -2),
        ]
        for float_1, float_2, value in float_pairs:
            value_range = ValueRange.from_pair(float_1, float_2)
            self.assertEqual(value_range.lower(), min(float_1, float_2))
            self.assertEqual(value_range.upper(), max(float_1, float_2))
            value_range.extend(value)
            self.assertEqual(value_range.lower(), min(float_1, float_2, value))
            self.assertEqual(value_range.upper(), max(float_1, float_2, value))

    def test_interpolate_with_invalid_raises_exception(self) -> None:
        value_range = ValueRange()
        self.assertFalse(value_range.is_valid())
        with self.assertRaises(ValueError):
            value_range.interpolate(1.0)

    def test_interpolate_with_valid_returns_value(self) -> None:
        float_pairs = [
            (0.0, 0.0, 0.0, 0.0),
            (0.0, 2.0, 1.0, 2.0),
            (-1.0, 0.0, 2.0, 1.0),
            (1.0, 0.0, -1.0, -1.0),
            (0.0, -1.0, 0.5, -0.5),
            (-1.0, 1.0, -2.0, -5.0),
        ]
        for float_1, float_2, value, expected in float_pairs:
            value_range = ValueRange.from_pair(float_1, float_2)
            self.assertEqual(value_range.interpolate(value), expected)

    def test_relative_position_with_invalid_raises_exception(self) -> None:
        value_range = ValueRange()
        self.assertFalse(value_range.is_valid())
        with self.assertRaises(ValueError):
            value_range.relative_position(1.0)

    def test_relative_position_with_valid_returns_zero(self) -> None:
        float_pairs = [
            (0.0, 0.0, 0.0, 0.0),
            (0.0, 2.0, 1.0, 0.5),
            (-1.0, 0.0, 2.0, 1.0),
            (1.0, 0.0, -1.0, 0.0),
            (1.0, 1.0, 0.5, 0.0),
            (0.0, -2.0, -0.5, 0.75),
            (-1.0, 1.0, -0.5, 0.25),
        ]
        for float_1, float_2, value, expected in float_pairs:
            value_range = ValueRange.from_pair(float_1, float_2)
            self.assertEqual(value_range.relative_position(value), expected)
