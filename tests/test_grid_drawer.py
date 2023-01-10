"""
Several tests for GridDrawer
"""
# Copyright 2022-2022 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from argparse import ArgumentParser
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from gpxtrackposter.grid_drawer import GridDrawer
from gpxtrackposter.exceptions import PosterError
from gpxtrackposter.poster import Poster
from gpxtrackposter.units import Units


@pytest.mark.full_run
def test_run_drawer(
    poster: Poster,
    grid_drawer: GridDrawer,
    parser: ArgumentParser,
    mock_track_instance_berlin_paris: MagicMock,
    mock_track_instance_amsterdam_paris: MagicMock,
    mocker: MockerFixture,
) -> None:
    mocker.patch("svgwrite.Drawing.save", return_value=True)

    grid_drawer.create_args(parser)
    args = parser.parse_args(["--type", "grid"])
    grid_drawer.fetch_args(args)
    grid_drawer.poster = poster
    poster.set_title("GridDrawer Test")
    assert poster.tracks_drawer is None
    poster.tracks_drawer = grid_drawer
    assert isinstance(poster.tracks_drawer, GridDrawer)
    assert len(poster.tracks) == 0

    # raises error without tracks
    with pytest.raises(PosterError):
        poster.draw(grid_drawer, args.output)

    poster.set_tracks([mock_track_instance_berlin_paris, mock_track_instance_amsterdam_paris])
    assert len(poster.tracks) != 0
    assert poster.length_range.lower() == 431.4 * Units().km
    assert poster.length_range.upper() == 884.0 * Units().km
    poster.draw(grid_drawer, args.output)


@pytest.mark.full_run
def test_run_drawer_with_animation(
    poster: Poster,
    grid_drawer: GridDrawer,
    parser: ArgumentParser,
    mock_track_instance_berlin_paris: MagicMock,
    mock_track_instance_amsterdam_paris: MagicMock,
    mocker: MockerFixture,
) -> None:
    mocker.patch("svgwrite.Drawing.save", return_value=True)

    grid_drawer.create_args(parser)
    args = parser.parse_args(["--type", "grid", "--with-animation"])
    grid_drawer.fetch_args(args)
    poster.set_title("GridDrawer Test")
    poster.tracks_drawer = grid_drawer
    grid_drawer.poster = poster
    assert not grid_drawer.poster.with_animation
    poster.set_with_animation(args.with_animation)
    assert grid_drawer.poster.with_animation
    poster.set_tracks([mock_track_instance_berlin_paris, mock_track_instance_amsterdam_paris])
    assert len(poster.tracks) != 0
    poster.draw(grid_drawer, args.output)
