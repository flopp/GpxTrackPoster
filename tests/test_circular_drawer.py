"""
Several tests for CircularDrawer
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from argparse import ArgumentParser

from pint.quantity import Quantity  # type: ignore

from gpxtrackposter.circular_drawer import CircularDrawer
from gpxtrackposter.cli import parse_args


def test_parser_with_type_circular_sets_type(circular_drawer: CircularDrawer, parser: ArgumentParser) -> None:
    circular_drawer.create_args(parser)
    parsed = parse_args(parser, ["--type", "circular"])
    assert parsed.type
    assert parsed.type == "circular"


def test_parser_without_rings_sets_false(circular_drawer: CircularDrawer, parser: ArgumentParser) -> None:
    circular_drawer.create_args(parser)
    parsed = parser.parse_args(["--type", "circular"])
    assert not parsed.circular_rings


def test_parser_with_rings_sets_true(circular_drawer: CircularDrawer, parser: ArgumentParser) -> None:
    circular_drawer.create_args(parser)
    parsed = parser.parse_args(["--type", "circular", "--circular-rings"])
    assert parsed.circular_rings


def test_parser_without_color_sets_color_darkgrey(circular_drawer: CircularDrawer, parser: ArgumentParser) -> None:
    circular_drawer.create_args(parser)
    parsed = parser.parse_args(["--type", "circular"])
    circular_drawer.fetch_args(parsed)
    assert parsed.circular_ring_color
    assert circular_drawer._ring_color == "darkgrey"  # pylint: disable=protected-access


def test_parser_with_color_sets_value(circular_drawer: CircularDrawer, parser: ArgumentParser) -> None:
    circular_drawer.create_args(parser)
    parsed = parser.parse_args(["--type", "circular", "--circular-ring-color", "red"])
    circular_drawer.fetch_args(parsed)
    assert parsed.circular_ring_color
    assert circular_drawer._ring_color == "red"  # pylint: disable=protected-access


def test_parser_without_distance_keeps_none(circular_drawer: CircularDrawer, parser: ArgumentParser) -> None:
    circular_drawer.create_args(parser)
    parsed = parser.parse_args(["--type", "circular"])
    circular_drawer.fetch_args(parsed)
    assert not parsed.circular_ring_max_distance
    assert circular_drawer._max_distance is None  # pylint: disable=protected-access


def test_parser_with_distance_sets_quantity_value(circular_drawer: CircularDrawer, parser: ArgumentParser) -> None:
    value = 10.0
    expected_value = Quantity(value, "km")
    circular_drawer.create_args(parser)
    parsed = parser.parse_args(["--type", "circular", "--circular-ring-max-distance", str(value)])
    circular_drawer.fetch_args(parsed)
    assert parsed.circular_ring_max_distance
    assert circular_drawer._max_distance == expected_value  # pylint: disable=protected-access
