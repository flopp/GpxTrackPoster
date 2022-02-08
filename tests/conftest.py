"""
ConfTest
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import argparse
import datetime
import os
from argparse import ArgumentParser
from typing import Generator
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from gpxtrackposter.calendar_drawer import CalendarDrawer
from gpxtrackposter.circular_drawer import CircularDrawer
from gpxtrackposter.cli import create_parser
from gpxtrackposter.github_drawer import GithubDrawer
from gpxtrackposter.grid_drawer import GridDrawer
from gpxtrackposter.heatmap_drawer import HeatmapDrawer
from gpxtrackposter.poster import Poster
from gpxtrackposter.units import Units


@pytest.fixture(scope="session")
def clear_files_teardown() -> Generator:
    """Session tear down"""
    yield None
    try:
        os.remove("poster.svg")
        os.remove("logger.log")
    except FileNotFoundError:
        pass


@pytest.fixture(name="default_values")
def fixture_default_values() -> argparse.Namespace:
    """Return default values as argparse.Namespace"""
    arguments = argparse.Namespace(
        gpx_dir=".",
        output="poster.svg",
        language="",
        localedir=None,
        year="all",
        athlete="John Doe",
        title=None,
        special=[],
        type="grid",
        background_color="#222222",
        track_color="#4DD2FF",
        track_color2=None,
        text_color="#FFFFFF",
        special_color="#FFFF00",
        special_color2=None,
        units="metric",
        clear_cache=False,
        verbose=False,
        special_distance=10.0,
        special_distance2=20.0,
        min_distance=1.0,
        activity_type="all",
        with_animation=False,
        animation_time=30,
        workers=None,
    )
    return arguments


@pytest.fixture(name="mock_track_instance")
def fixture_mock_track_instance(mocker: MockerFixture) -> MagicMock:
    """Fixture for Track"""
    mock_track_class = mocker.patch("gpxtrackposter.track_loader.Track")
    instance = mock_track_class.return_value
    instance.length.return_value = 1 * Units().km
    instance.start_time.return_value = datetime.datetime.now()
    instance.end_time.return_value = datetime.datetime.now()
    return instance


@pytest.fixture(name="mock_track_instance_1")
def fixture_mock_track_instance_1(mocker: MockerFixture) -> MagicMock:
    """Fixture for Track 1"""
    mock_track_class = mocker.patch("gpxtrackposter.track_loader.Track")
    instance = mock_track_class.return_value
    instance.length.return_value = 1 * Units().km
    instance.start_time.return_value = datetime.datetime.now()
    instance.end_time.return_value = datetime.datetime.now()
    return instance


@pytest.fixture(name="mock_track_instance_2")
def fixture_mock_track_instance_2(mocker: MockerFixture) -> MagicMock:
    """Fixture for Track 2"""
    mock_track_class = mocker.patch("gpxtrackposter.track_loader.Track")
    instance = mock_track_class.return_value
    instance.length.return_value = 2 * Units().km
    instance.start_time.return_value = datetime.datetime.now()
    instance.end_time.return_value = datetime.datetime.now()
    return instance


@pytest.fixture(name="parser")
def fixture_parser() -> ArgumentParser:
    """Return an ArgParser"""
    return create_parser()


@pytest.fixture(name="calendar_drawer")
def fixture_calendar_drawer() -> CalendarDrawer:
    """Return a CalendarDrawer"""
    return CalendarDrawer(Poster())


@pytest.fixture(name="circular_drawer")
def fixture_circular_drawer() -> CircularDrawer:
    """Return a CircularDrawer"""
    return CircularDrawer(Poster())


@pytest.fixture(name="github_drawer")
def fixture_github_drawer() -> GithubDrawer:
    """Return a GithubDrawer"""
    return GithubDrawer(Poster())


@pytest.fixture(name="grid_drawer")
def fixture_grid_drawer() -> GridDrawer:
    """Return a GridDrawer"""
    return GridDrawer(Poster())


@pytest.fixture(name="heatmap_drawer")
def fixture_heatmap_drawer() -> HeatmapDrawer:
    """Return a HeatmapDrawer"""
    return HeatmapDrawer(Poster())
