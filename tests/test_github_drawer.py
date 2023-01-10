"""
Several tests for GithubDrawer
"""
# Copyright 2022-2023 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from argparse import ArgumentParser
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from gpxtrackposter.github_drawer import GithubDrawer
from gpxtrackposter.exceptions import PosterError
from gpxtrackposter.poster import Poster
from gpxtrackposter.units import Units


@pytest.mark.full_run
def test_run_drawer(
    poster: Poster,
    github_drawer: GithubDrawer,
    parser: ArgumentParser,
    mock_track_instance_berlin_paris: MagicMock,
    mock_track_instance_amsterdam_paris: MagicMock,
    mocker: MockerFixture,
) -> None:
    mocker.patch("svgwrite.Drawing.save", return_value=True)

    github_drawer.create_args(parser)
    args = parser.parse_args([])
    github_drawer.fetch_args(args)
    github_drawer.poster = poster
    poster.set_title("GithubDrawer Test")
    assert poster.tracks_drawer is None
    poster.tracks_drawer = github_drawer
    assert isinstance(poster.tracks_drawer, GithubDrawer)
    assert len(poster.tracks) == 0

    # raises error without tracks
    with pytest.raises(PosterError):
        poster.draw(github_drawer, args.output)

    poster.set_tracks([mock_track_instance_berlin_paris, mock_track_instance_amsterdam_paris])
    assert len(poster.tracks) != 0
    assert poster.length_range.lower() == 431.4 * Units().km
    assert poster.length_range.upper() == 884.0 * Units().km
    poster.draw(github_drawer, args.output)


@pytest.mark.full_run
def test_run_drawer_with_animation(
    poster: Poster,
    github_drawer: GithubDrawer,
    parser: ArgumentParser,
    mock_track_instance_berlin_paris: MagicMock,
    mock_track_instance_amsterdam_paris: MagicMock,
    mocker: MockerFixture,
) -> None:
    mocker.patch("svgwrite.Drawing.save", return_value=True)

    github_drawer.create_args(parser)
    args = parser.parse_args(["--with-animation"])
    github_drawer.fetch_args(args)
    poster.set_title("GithubDrawer Test")
    poster.tracks_drawer = github_drawer
    github_drawer.poster = poster
    assert not github_drawer.poster.with_animation
    poster.set_with_animation(args.with_animation)
    assert github_drawer.poster.with_animation
    poster.set_tracks([mock_track_instance_berlin_paris, mock_track_instance_amsterdam_paris])
    assert len(poster.tracks) != 0
    poster.draw(github_drawer, args.output)
