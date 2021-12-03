"""
Several tests for XY
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from typing import List, Tuple, Union
import unittest
from gpxtrackposter.xy import XY


class TestCase(unittest.TestCase):
    """
    Test class for YearRange
    """

    def test_multiplication(self) -> None:
        test_object: XY = XY(50.0, 100.0)
        test_values: List[Union[Tuple[float, Tuple[float, float]], Tuple[XY, Tuple[float, float]]]] = [
            (10.0, (500.0, 1000.0)),
            (10, (500.0, 1000.0)),
            (0.5, (25.0, 50.0)),
            (-5.0, (-250.0, -500.0)),
            (XY(10.0, 5.0), (500.0, 500.0)),
            (XY(-10.0, 5.0), (-500.0, 500.0)),
            (XY(0.5, -5.0), (25.0, -500.0)),
        ]
        for other, result in test_values:
            self.assertEqual((test_object * other).tuple(), result)

    def test_division(self) -> None:
        test_object: XY = XY(50.0, 100.0)
        test_values: List[Union[Tuple[float, Tuple[float, float]], Tuple[XY, Tuple[float, float]]]] = [
            (10.0, (5.0, 10.0)),
            (10, (5.0, 10.0)),
            (0.5, (100.0, 200.0)),
            (-5.0, (-10.0, -20.0)),
            (XY(10.0, 5.0), (5.0, 20.0)),
            (XY(-10.0, 5.0), (-5.0, 20.0)),
            (XY(0.5, -5.0), (100.0, -20.0)),
        ]
        for other, result in test_values:
            self.assertEqual((test_object / other).tuple(), result)

    def test_addition(self) -> None:
        test_object: XY = XY(50.0, 100.0)
        test_values: List[Union[Tuple[float, Tuple[float, float]], Tuple[XY, Tuple[float, float]]]] = [
            (10.0, (60.0, 110.0)),
            (10, (60.0, 110.0)),
            (0.5, (50.5, 100.5)),
            (-5.0, (45.0, 95.0)),
            (XY(10.0, 5.0), (60.0, 105.0)),
            (XY(-10.0, 5.0), (40.0, 105.0)),
            (XY(0.5, -5.0), (50.5, 95.0)),
        ]
        for other, result in test_values:
            self.assertEqual((test_object + other).tuple(), result)

    def test_subtraction(self) -> None:
        test_object: XY = XY(50.0, 100.0)
        test_values: List[Union[Tuple[float, Tuple[float, float]], Tuple[XY, Tuple[float, float]]]] = [
            (10.0, (40.0, 90.0)),
            (10, (40.0, 90.0)),
            (0.5, (49.5, 99.5)),
            (-5.0, (55.0, 105.0)),
            (XY(10.0, 5.0), (40.0, 95.0)),
            (XY(-10.0, 5.0), (60.0, 95.0)),
            (XY(0.5, -5.0), (49.5, 105.0)),
        ]
        for other, result in test_values:
            self.assertEqual((test_object - other).tuple(), result)

    def test_representation(self) -> None:
        test_object: XY = XY(50.0, 100.0)
        self.assertEqual(str(test_object), "XY: 50.0/100.0")

    def test_tuple(self) -> None:
        test_object: XY = XY(50.0, 100.0)
        self.assertEqual(test_object.tuple(), (50.0, 100.0))

    def test_to_int(self) -> None:
        test_object: XY = XY(50.12345, 100.98765)
        self.assertEqual(test_object.to_int().tuple(), (50, 100))

    def test_round(self) -> None:
        test_object: XY = XY(50.12345, 100.98765)
        test_values: List[Union[Tuple[int, Tuple[float, float]], Tuple[None, Tuple[float, float]]]] = [
            (0, (50.0, 101.0)),
            (1, (50.1, 101.0)),
            (2, (50.12, 100.99)),
            (3, (50.123, 100.988)),
            (4, (50.1234, 100.9877)),
            (5, (50.12345, 100.98765)),
            (None, (50.0, 101.0)),
        ]
        for n, result in test_values:
            self.assertEqual(test_object.round(n).tuple(), result)

    def test_get_max(self) -> None:
        test_values: List[Tuple[XY, Union[int, float]]] = [
            (XY(12.5, 25.0), 25.0),
            (XY(25.0, 12.5), 25.0),
            (XY(12.5, -25.0), 12.5),
            (XY(-25.0, 12.5), 12.5),
            (XY(12, 25), 25),
            (XY(25, 12), 25),
        ]
        for test_object, result in test_values:
            self.assertEqual(test_object.get_max(), result)

    def test_get_min(self) -> None:
        test_values: List[Tuple[XY, Union[int, float]]] = [
            (XY(12.5, 25.0), 12.5),
            (XY(25.0, 12.5), 12.5),
            (XY(12.5, -25.0), -25.0),
            (XY(-25.0, 12.5), -25.0),
            (XY(12, 25), 12),
            (XY(25, 12), 12),
        ]
        for test_object, result in test_values:
            self.assertEqual(test_object.get_min(), result)

    def test_scale_to_max_value(self) -> None:
        test_object: XY = XY(50.0, 100.0)
        good_values: List[Tuple[float, Tuple[float, float]]] = [
            (25.0, (12.5, 25.0)),
            (50.0, (25.0, 50.0)),
            (200.0, (100.0, 200.0)),
            (-50.0, (-25.0, -50.0)),
        ]
        bad_values: List[Tuple[float, Tuple[float, float]]] = [
            (25.0, (25.0, 12.5)),
            (-50.0, (25.0, -50.0)),
            (-50.0, (-25.0, 50.0)),
        ]
        for max_value, result in good_values:
            self.assertEqual(test_object.scale_to_max_value(max_value).tuple(), result)

        for max_value, result in bad_values:
            self.assertNotEqual(test_object.scale_to_max_value(max_value).tuple(), result)

    def test_scale_to_max_value_with_x_gt_y(self) -> None:
        test_object: XY = XY(100.0, 50.0)
        good_values: List[Tuple[float, Tuple[float, float]]] = [
            (25.0, (25.0, 12.5)),
            (50.0, (50.0, 25.0)),
            (200.0, (200.0, 100.0)),
            (-50.0, (-50.0, -25.0)),
        ]
        bad_values: List[Tuple[float, Tuple[float, float]]] = [
            (25.0, (12.5, 25.0)),
            (-50.0, (50.0, -25.0)),
            (-50.0, (-50.0, 25.0)),
        ]
        for max_value, result in good_values:
            self.assertEqual(test_object.scale_to_max_value(max_value).tuple(), result)

        for max_value, result in bad_values:
            self.assertNotEqual(test_object.scale_to_max_value(max_value).tuple(), result)


if __name__ == "__main__":
    unittest.main()
