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
        """clear returns invalid and empty instance of ValueRange"""
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
        """lower returns the lower value of ValueRange"""
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
        """upper returns the lower value of ValueRange"""
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
        """diameter returns the difference of upper and lower"""
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

    def test_diameter_on_invalid_returns_zero(self) -> None:
        """diameter on invalid instance returns 0"""
        value_range = ValueRange()
        self.assertFalse(value_range.is_valid())
        self.assertEqual(value_range.diameter(), 0.0)

    def test_contains_returns_true(self) -> None:
        """contains returns True"""
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
        """contains returns False"""
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

    def test_contains_on_invalid_returns_false(self) -> None:
        """contains on invalid instance returns False"""
        value_range = ValueRange()
        self.assertFalse(value_range.is_valid())
        self.assertFalse(value_range.contains(1.0))

    def test_extend_on_invalid_instance_instance_returns_valid(self) -> None:
        """extend on invalid instance returns valid instance with upper and lower"""
        value = 1.0
        value_range = ValueRange()
        self.assertFalse(value_range.is_valid())
        value_range.extend(value)
        self.assertTrue(value_range.is_valid())
        self.assertEqual(value_range.lower(), value)
        self.assertEqual(value_range.upper(), value)

    def test_extend_returns_extended_value_range(self) -> None:
        """extend returns a ValueRange with extended upper and/or lower"""
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

    def test_interpolate_on_invalid_instance_raises_exception(self) -> None:
        """interpolate on invalid instance raises exception"""
        value_range = ValueRange()
        self.assertFalse(value_range.is_valid())
        with self.assertRaises(ValueError):
            value_range.interpolate(1.0)

    def test_interpolate_on_valid_instance_returns_value(self) -> None:
        """interpolate returns interpolated value"""
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

    def test_relative_position_on_invalid_instance_raises_exception(self) -> None:
        """relative_position on invalid instance raises exception"""
        value_range = ValueRange()
        self.assertFalse(value_range.is_valid())
        with self.assertRaises(ValueError):
            value_range.relative_position(1.0)

    def test_relative_position_on_valid_instance_returns_expected_value(self) -> None:
        """relative_position returns the relative position value"""
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


if __name__ == '__main__':
    unittest.main()
