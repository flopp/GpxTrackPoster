"""
Several tests for QuantityRange
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import unittest

from pint.quantity import Quantity  # type: ignore

from gpxtrackposter.quantity_range import QuantityRange


class TestCase(unittest.TestCase):
    """
    Test class for QuantityRange
    """

    def test_init_returns_invalid_instance(self) -> None:
        """QuantityRange object is initialised with None values, thus invalid"""
        value_range = QuantityRange()
        self.assertFalse(value_range.is_valid())

    def test_from_pair_returns_instance(self) -> None:
        """from_pair returns instance of QuantityRange"""
        value_range = QuantityRange.from_pair(Quantity(0.0), Quantity(0.0))
        self.assertTrue(value_range.is_valid())
        self.assertIsInstance(value_range, QuantityRange)

    def test_clear_returns_invalid_empty_instance(self) -> None:
        float_pairs = [(0.0, 0.0), (0.0, 1.0), (-1.0, 0.0)]
        for float_1, float_2 in float_pairs:
            value_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertTrue(value_range.is_valid())
            self.assertEqual(value_range.lower(), Quantity(float_1))
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
            value_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertEqual(value_range.lower(), min(Quantity(float_1), Quantity(float_2)))
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
            value_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertEqual(value_range.upper(), max(Quantity(float_1), Quantity(float_2)))
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
            value_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
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
            value_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertTrue(value_range.contains(Quantity(value)))

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
            value_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertFalse(value_range.contains(Quantity(value)))

    def test_extend_with_invalid_instance_returns_valid(self) -> None:
        value = 1.0
        value_range = QuantityRange()
        self.assertFalse(value_range.is_valid())
        value_range.extend(Quantity(value))
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
            value_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertEqual(value_range.lower(), Quantity(min(float_1, float_2)))
            self.assertEqual(value_range.upper(), Quantity(max(float_1, float_2)))
            value_range.extend(Quantity(value))
            self.assertEqual(value_range.lower(), Quantity(min(float_1, float_2, value)))
            self.assertEqual(value_range.upper(), Quantity(max(float_1, float_2, value)))

    def test_interpolate_with_invalid_raises_exception(self) -> None:
        value_range = QuantityRange()
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
            value_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertEqual(value_range.interpolate(value), expected)

    def test_relative_position_with_invalid_raises_exception(self) -> None:
        value_range = QuantityRange()
        self.assertFalse(value_range.is_valid())
        with self.assertRaises(ValueError):
            value_range.relative_position(Quantity(1.0))

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
            value_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertEqual(value_range.relative_position(Quantity(value)), expected)
