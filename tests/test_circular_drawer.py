"""
Several tests for CircularDrawer
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import unittest

from pint.quantity import Quantity  # type: ignore

from gpxtrackposter.circular_drawer import CircularDrawer
from gpxtrackposter.cli import create_parser, parse_args
from gpxtrackposter.poster import Poster


class TestCase(unittest.TestCase):
    """
    Test class for CircularDrawer
    """

    def setUp(self) -> None:
        self.poster = Poster()
        self.circular_drawer = CircularDrawer(self.poster)
        self.parser = create_parser()

    def test_parser_with_type_circular_sets_type(self) -> None:
        self.circular_drawer.create_args(self.parser)
        parsed = parse_args(self.parser, ["--type", "circular"])
        self.assertTrue(parsed.type)
        self.assertEqual(parsed.type, "circular")

    def test_parser_without_rings_sets_false(self) -> None:
        self.circular_drawer.create_args(self.parser)
        parsed = self.parser.parse_args(["--type", "circular"])
        self.assertFalse(parsed.circular_rings)

    def test_parser_with_rings_sets_true(self) -> None:
        self.circular_drawer.create_args(self.parser)
        parsed = self.parser.parse_args(["--type", "circular", "--circular-rings"])
        self.assertTrue(parsed.circular_rings)

    def test_parser_without_color_sets_color_darkgrey(self) -> None:
        self.circular_drawer.create_args(self.parser)
        parsed = self.parser.parse_args(["--type", "circular"])
        self.circular_drawer.fetch_args(parsed)
        self.assertTrue(parsed.circular_ring_color)
        self.assertEqual(self.circular_drawer._ring_color, "darkgrey")  # pylint: disable=protected-access

    def test_parser_with_color_sets_value(self) -> None:
        self.circular_drawer.create_args(self.parser)
        parsed = self.parser.parse_args(["--type", "circular", "--circular-ring-color", "red"])
        self.circular_drawer.fetch_args(parsed)
        self.assertTrue(parsed.circular_ring_color)
        self.assertEqual(self.circular_drawer._ring_color, "red")  # pylint: disable=protected-access

    def test_parser_without_distance_keeps_none(self) -> None:
        self.circular_drawer.create_args(self.parser)
        parsed = self.parser.parse_args(["--type", "circular"])
        self.circular_drawer.fetch_args(parsed)
        self.assertFalse(parsed.circular_ring_max_distance)
        self.assertIsNone(self.circular_drawer._max_distance)  # pylint: disable=protected-access

    def test_parser_with_distance_sets_quantity_value(self) -> None:
        value = 10.0
        expected_value = Quantity(value, "km")
        self.circular_drawer.create_args(self.parser)
        parsed = self.parser.parse_args(["--type", "circular", "--circular-ring-max-distance", str(value)])
        self.circular_drawer.fetch_args(parsed)
        self.assertTrue(parsed.circular_ring_max_distance)
        self.assertEqual(self.circular_drawer._max_distance, expected_value)  # pylint: disable=protected-access


if __name__ == "__main__":
    unittest.main()
