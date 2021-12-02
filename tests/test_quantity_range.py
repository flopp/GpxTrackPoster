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
        quantity_range = QuantityRange()
        self.assertFalse(quantity_range.is_valid())

    def test_from_pair_returns_instance(self) -> None:
        """from_pair returns instance of QuantityRange"""
        quantity_range = QuantityRange.from_pair(Quantity(0.0), Quantity(0.0))
        self.assertTrue(quantity_range.is_valid())
        self.assertIsInstance(quantity_range, QuantityRange)

    def test_clear_returns_invalid_empty_instance(self) -> None:
        """clear returns invalid and empty instance of QuantityRange"""
        float_pairs = [(0.0, 0.0), (0.0, 1.0), (-1.0, 0.0)]
        for float_1, float_2 in float_pairs:
            quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertTrue(quantity_range.is_valid())
            self.assertEqual(quantity_range.lower(), Quantity(float_1))
            quantity_range.clear()
            self.assertFalse(quantity_range.is_valid())
            self.assertEqual(quantity_range.lower(), None)
            self.assertEqual(quantity_range.upper(), None)

    def test_lower_returns_lower_value(self) -> None:
        """lower returns a Quantity instance of the lower value"""
        float_pairs = [
            (0.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (-1.0, 0.0, -1.0),
            (1.0, 0.0, 0.0),
            (0.0, -1.0, -1.0),
            (-1.0, 1.0, -1.0),
        ]
        for float_1, float_2, lower in float_pairs:
            quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertEqual(quantity_range.lower(), Quantity(min(float_1, float_2)))
            self.assertEqual(quantity_range.lower(), Quantity(lower))
            self.assertEqual(quantity_range.lower(), lower)

    def test_upper_returns_upper_value(self) -> None:
        """upper returns a Quantity instance of the lower value"""
        float_pairs = [
            (0.0, 0.0, 0.0),
            (0.0, 1.0, 1.0),
            (-1.0, 0.0, 0.0),
            (1.0, 0.0, 1.0),
            (0.0, -1.0, 0.0),
            (-1.0, 1.0, 1.0),
        ]
        for float_1, float_2, upper in float_pairs:
            quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertEqual(quantity_range.upper(), Quantity(max(float_1, float_2)))
            self.assertEqual(quantity_range.upper(), Quantity(upper))
            self.assertEqual(quantity_range.upper(), upper)

    def test_diameter_returns_difference(self) -> None:
        """diameter returns a Quantity of the difference of upper and lower"""
        float_pairs = [
            (0.0, 0.0, 0.0),
            (0.0, 1.0, 1.0),
            (-1.0, 0.0, 1.0),
            (1.0, 0.0, 1.0),
            (0.0, -1.0, 1.0),
            (-1.0, 1.0, 2.0),
        ]
        for float_1, float_2, difference in float_pairs:
            quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertEqual(quantity_range.diameter(), Quantity(difference))
            self.assertEqual(quantity_range.diameter(), difference)

    def test_diameter_on_invalid_returns_zero(self) -> None:
        """diameter on invalid instance returns Quantity(0)"""
        quantity_range = QuantityRange()
        self.assertFalse(quantity_range.is_valid())
        self.assertEqual(quantity_range.diameter(), Quantity(0.0))
        self.assertEqual(quantity_range.diameter(), 0.0)

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
            quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertTrue(quantity_range.contains(Quantity(value)))

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
            quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertFalse(quantity_range.contains(Quantity(value)))

    def test_contains_on_invalid_returns_false(self) -> None:
        """contains on invalid instance returns False"""
        quantity_range = QuantityRange()
        self.assertFalse(quantity_range.is_valid())
        self.assertFalse(quantity_range.contains(Quantity(1.0)))

    def test_extend_on_invalid_instance_instance_returns_valid(self) -> None:
        """extend on invalid instance returns valid instance with upper and lower"""
        value = 1.0
        quantity_range = QuantityRange()
        self.assertFalse(quantity_range.is_valid())
        quantity_range.extend(Quantity(value))
        self.assertTrue(quantity_range.is_valid())
        self.assertEqual(quantity_range.lower(), Quantity(value))
        self.assertEqual(quantity_range.upper(), Quantity(value))
        self.assertEqual(quantity_range.lower(), value)
        self.assertEqual(quantity_range.upper(), value)

    def test_extend_returns_extended_quantity_range(self) -> None:
        """extend returns a QuantityRange with extended upper and/or lower"""
        float_pairs = [
            (0.0, 0.0, 1.0),
            (0.0, 1.0, 2.0),
            (-1.0, 0.0, 2.0),
            (1.0, 0.0, -1.0),
            (0.0, -1.0, 0.5),
            (-1.0, 1.0, -2),
        ]
        for float_1, float_2, value in float_pairs:
            quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertEqual(quantity_range.lower(), Quantity(min(float_1, float_2)))
            self.assertEqual(quantity_range.upper(), Quantity(max(float_1, float_2)))
            quantity_range.extend(Quantity(value))
            self.assertEqual(quantity_range.lower(), Quantity(min(float_1, float_2, value)))
            self.assertEqual(quantity_range.upper(), Quantity(max(float_1, float_2, value)))
            self.assertEqual(quantity_range.lower(), min(float_1, float_2, value))
            self.assertEqual(quantity_range.upper(), max(float_1, float_2, value))

    def test_interpolate_on_invalid_instance_raises_exception(self) -> None:
        """interpolate on invalid instance raises exception"""
        quantity_range = QuantityRange()
        self.assertFalse(quantity_range.is_valid())
        with self.assertRaises(ValueError):
            quantity_range.interpolate(1.0)

    def test_interpolate_on_valid_instance_returns_value(self) -> None:
        """interpolate returns a Quantity with interpolated value"""
        float_pairs = [
            (0.0, 0.0, 0.0, 0.0),
            (0.0, 2.0, 1.0, 2.0),
            (-1.0, 0.0, 2.0, 1.0),
            (1.0, 0.0, -1.0, -1.0),
            (0.0, -1.0, 0.5, -0.5),
            (-1.0, 1.0, -2.0, -5.0),
        ]
        for float_1, float_2, value, expected in float_pairs:
            quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertEqual(quantity_range.interpolate(value), Quantity(expected))
            self.assertEqual(quantity_range.interpolate(value), expected)

    def test_relative_position_on_invalid_instance_raises_exception(self) -> None:
        """relative_position on invalid instance raises exception"""
        quantity_range = QuantityRange()
        self.assertFalse(quantity_range.is_valid())
        with self.assertRaises(ValueError):
            quantity_range.relative_position(Quantity(1.0))

    def test_relative_position_on_valid_instance_returns_expected_value(self) -> None:
        """relative_position returns a Quantity of the relative position value"""
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
            quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
            self.assertEqual(quantity_range.relative_position(Quantity(value)), Quantity(expected))
            self.assertEqual(quantity_range.relative_position(Quantity(value)), expected)


if __name__ == '__main__':
    unittest.main()
