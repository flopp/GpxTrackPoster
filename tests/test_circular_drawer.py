"""
Several tests for CircularDrawer
"""
# Copyright 2021-2023 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from argparse import ArgumentParser
from unittest.mock import MagicMock

import pytest
from pint import Quantity  # type: ignore
from pytest_mock import MockerFixture

from gpxtrackposter.circular_drawer import CircularDrawer
from gpxtrackposter.cli import parse_args
from gpxtrackposter.exceptions import PosterError
from gpxtrackposter.poster import Poster
from gpxtrackposter.units import Units


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
    parsed = parser.parse_args(["--circular-rings"])
    assert parsed.circular_rings


def test_parser_without_color_sets_color_darkgrey(circular_drawer: CircularDrawer, parser: ArgumentParser) -> None:
    circular_drawer.create_args(parser)
    parsed = parser.parse_args(["--type", "circular"])
    circular_drawer.fetch_args(parsed)
    assert parsed.circular_ring_color
    assert circular_drawer._ring_color == "darkgrey"  # pylint: disable=protected-access


def test_parser_with_color_sets_value(circular_drawer: CircularDrawer, parser: ArgumentParser) -> None:
    circular_drawer.create_args(parser)
    parsed = parser.parse_args(["--circular-ring-color", "red"])
    circular_drawer.fetch_args(parsed)
    assert parsed.circular_ring_color
    assert circular_drawer._ring_color == "red"  # pylint: disable=protected-access


def test_parser_without_distance_keeps_none(circular_drawer: CircularDrawer, parser: ArgumentParser) -> None:
    circular_drawer.create_args(parser)
    parsed = parser.parse_args(["--type", "circular"])
    circular_drawer.fetch_args(parsed)
    assert not parsed.circular_ring_max_distance
    assert circular_drawer._max_distance is None  # pylint: disable=protected-access


@pytest.mark.parametrize(
    "units, value, expected_value",
    [
        ("imperial", 1.0, 1.0 / 1.609344 * Units().mi),
        ("imperial", 5.0, 5.0 / 1.609344 * Units().mi),
        ("imperial", 10.0, 10.0 / 1.609344 * Units().mi),
        ("imperial", 50.0, 50.0 / 1.609344 * Units().mi),
        ("metric", 1.0, 1.0 * Units().km),
        ("metric", 5.0, 5.0 * Units().km),
        ("metric", 10.0, 10.0 * Units().km),
        ("metric", 50.0, 50.0 * Units().km),
    ],
)
def test_parser_with_distance_sets_quantity_value(
    units: str, value: float, expected_value: Quantity, circular_drawer: CircularDrawer, parser: ArgumentParser
) -> None:
    circular_drawer.create_args(parser)
    parsed = parser.parse_args(["--circular-ring-max-distance", str(value), "--unit", units])
    circular_drawer.fetch_args(parsed)
    assert parsed.circular_ring_max_distance
    assert circular_drawer._max_distance == expected_value.to("mi")  # pylint: disable=protected-access
    assert circular_drawer._max_distance == expected_value.to("km")  # pylint: disable=protected-access


@pytest.mark.parametrize(
    "units, value, expected_value",
    [
        ("imperial", 0.9 * Units().mi, None),
        ("imperial", 1.1 * Units().mi, 1.0 * Units().mi),
        ("imperial", 4.9 * Units().mi, 1.0 * Units().mi),
        ("imperial", 5.1 * Units().mi, 5.0 * Units().mi),
        ("imperial", 9.9 * Units().mi, 5.0 * Units().mi),
        ("imperial", 10.1 * Units().mi, 5.0 * Units().mi),
        ("imperial", 49.9 * Units().mi, 10.0 * Units().mi),
        ("imperial", 50.1 * Units().mi, 50.0 * Units().mi),
        ("metric", 0.9 * Units().km, None),
        ("metric", 1.1 * Units().km, 1.0 * Units().km),
        ("metric", 4.9 * Units().km, 1.0 * Units().km),
        ("metric", 5.1 * Units().km, 5.0 * Units().km),
        ("metric", 9.9 * Units().km, 5.0 * Units().km),
        ("metric", 10.1 * Units().km, 5.0 * Units().km),
        ("metric", 49.9 * Units().km, 10.0 * Units().km),
        ("metric", 50.1 * Units().km, 50.0 * Units().km),
    ],
)
def test_determine_ring_distance(
    units: str, value: Quantity, expected_value: Quantity, circular_drawer: CircularDrawer, parser: ArgumentParser
) -> None:
    circular_drawer.poster.units = units
    circular_drawer.create_args(parser)
    circular_drawer.fetch_args(parser.parse_args([]))
    assert expected_value == circular_drawer._determine_ring_distance(value)  # pylint: disable=protected-access


@pytest.mark.full_run
def test_run_drawer(
    poster: Poster,
    circular_drawer: CircularDrawer,
    parser: ArgumentParser,
    mock_track_instance_berlin_paris: MagicMock,
    mock_track_instance_amsterdam_paris: MagicMock,
    mocker: MockerFixture,
) -> None:
    mocker.patch("svgwrite.Drawing.save", return_value=True)

    circular_drawer.create_args(parser)
    args = parser.parse_args(["--type", "circular"])
    circular_drawer.fetch_args(args)
    circular_drawer.poster = poster
    poster.set_title("CircularDrawer Test")
    assert poster.tracks_drawer is None
    poster.tracks_drawer = circular_drawer
    assert isinstance(poster.tracks_drawer, CircularDrawer)
    assert len(poster.tracks) == 0

    # raises error without tracks
    with pytest.raises(PosterError):
        poster.draw(circular_drawer, args.output)

    poster.set_tracks([mock_track_instance_berlin_paris, mock_track_instance_amsterdam_paris])
    assert len(poster.tracks) != 0
    assert poster.length_range.lower() == 431.4 * Units().km
    assert poster.length_range.upper() == 884.0 * Units().km
    poster.draw(circular_drawer, args.output)


@pytest.mark.full_run
def test_run_drawer_with_animation(
    poster: Poster,
    circular_drawer: CircularDrawer,
    parser: ArgumentParser,
    mock_track_instance_berlin_paris: MagicMock,
    mock_track_instance_amsterdam_paris: MagicMock,
    mocker: MockerFixture,
) -> None:
    mocker.patch("svgwrite.Drawing.save", return_value=True)

    circular_drawer.create_args(parser)
    args = parser.parse_args(
        ["--circular-rings", "--circular-ring-max-distance", "5.0", "--with-animation"]
    )
    circular_drawer.fetch_args(args)
    poster.set_title("CircularDrawer Test")
    poster.tracks_drawer = circular_drawer
    circular_drawer.poster = poster
    assert not circular_drawer.poster.with_animation
    poster.set_with_animation(args.with_animation)
    assert circular_drawer.poster.with_animation
    poster.set_tracks([mock_track_instance_berlin_paris, mock_track_instance_amsterdam_paris])
    assert len(poster.tracks) != 0
    poster.draw(circular_drawer, args.output)
