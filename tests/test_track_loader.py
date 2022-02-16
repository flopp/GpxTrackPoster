"""
Several tests for TrackLoader
"""
# Copyright 2020-2022 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import json
import os
from pathlib import Path
from typing import Union, Dict, List
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from gpxtrackposter.exceptions import ParameterError
from gpxtrackposter.track_loader import TrackLoader
from gpxtrackposter.units import Units
from gpxtrackposter.year_range import YearRange


def mock_activity(mocker: MockerFixture, activity_type: Union[str, list]) -> MagicMock:
    """Mock Activity"""
    activity = mocker.MagicMock()
    activity.type = activity_type
    return activity


@pytest.fixture(name="mock_run_activity")
def fixture_mock_run_activity(mocker: MockerFixture) -> MagicMock:
    """Mock Run Activity"""
    return mock_activity(mocker, "Run")


@pytest.fixture(name="mock_walk_activity")
def fixture_mock_walk_activity(mocker: MockerFixture) -> MagicMock:
    """Mock Walk Activity"""
    return mock_activity(mocker, "Walk")


@pytest.fixture(name="mock_hike_activity")
def fixture_mock_hike_activity(mocker: MockerFixture) -> MagicMock:
    """Mock Hike Activity"""
    return mock_activity(mocker, "Hike")


def strava_config(tmp_path: Path, activity_type: Union[str, List[str]] = None) -> str:
    """Strava config"""
    config: Dict[str, Union[str, List[str]]] = {
        "client_id": "YOUR STRAVA API CLIENT ID",
        "client_secret": "YOUR STRAVA API CLIENT SECRET",
        "refresh_token": "YOUR STRAVA REFRESH TOKEN",
    }
    if activity_type:
        config["activity_type"] = activity_type
    config_json = tmp_path / "strava-config.json"
    config_json.write_text(json.dumps(config))
    return str(config_json)


@pytest.fixture(name="strava_config_without_type_filter")
def fixture_strava_config_without_type_filter(tmp_path: Path) -> str:
    """Fixture Strava config without type filter"""
    return strava_config(tmp_path)


@pytest.fixture(name="strava_config_with_run_type_filter")
def fixture_strava_config_with_run_type_filter(tmp_path: Path) -> str:
    """Fixture Strava config without run type filter"""
    return strava_config(tmp_path, "Run")


@pytest.fixture(name="strava_config_with_walk_hike_type_filter")
def fixture_strava_config_with_walk_hike_type_filter(tmp_path: Path) -> str:
    """Fixture Strava config without walk and hike type filter"""
    return strava_config(tmp_path, ["Walk", "Hike"])


@pytest.fixture(name="loader")
def fixture_loader(
    mocker: MockerFixture, mock_run_activity: MagicMock, mock_walk_activity: MagicMock, mock_hike_activity: MagicMock
) -> TrackLoader:
    """Return a :class:`gpxtrackposter.track_loader.TrackLoader` object."""
    mock_client_class = mocker.patch("gpxtrackposter.track_loader.Client")
    instance = mock_client_class.return_value
    instance.get_activities.return_value = [mock_run_activity, mock_walk_activity, mock_hike_activity]
    return TrackLoader(workers=None)


def test_load_strava_tracks_without_activity_type_filter(
    loader: TrackLoader,
    strava_config_without_type_filter: str,
    mock_track_instance: MagicMock,
    mock_run_activity: MagicMock,
    mock_walk_activity: MagicMock,
    mock_hike_activity: MagicMock,
) -> None:
    loader.load_strava_tracks(strava_config_without_type_filter)

    mock_track_instance.load_strava.assert_any_call(mock_run_activity)
    mock_track_instance.load_strava.assert_any_call(mock_walk_activity)
    mock_track_instance.load_strava.assert_any_call(mock_hike_activity)


def test_load_strava_tracks_with_str_activity_type_filter(
    loader: TrackLoader,
    strava_config_with_run_type_filter: str,
    mock_track_instance: MagicMock,
    mock_run_activity: MagicMock,
) -> None:
    loader.load_strava_tracks(strava_config_with_run_type_filter)

    mock_track_instance.load_strava.assert_called_once_with(mock_run_activity)


def test_load_strava_tracks_with_list_activity_type_filter(
    loader: TrackLoader,
    strava_config_with_walk_hike_type_filter: str,
    mock_track_instance: MagicMock,
    mock_walk_activity: MagicMock,
    mock_hike_activity: MagicMock,
) -> None:
    loader.load_strava_tracks(strava_config_with_walk_hike_type_filter)

    mock_track_instance.load_strava.assert_any_call(mock_walk_activity)
    mock_track_instance.load_strava.assert_any_call(mock_hike_activity)


def test_init() -> None:
    loader = TrackLoader(workers=1)
    assert len(loader.special_file_names) == 0
    assert loader.year_range == YearRange()
    assert not loader.cache_dir
    assert not loader.strava_cache_file


def test_gpx_no_dir() -> None:
    """Temporary gpx directory - no directory"""
    no_dir = "this_dir_does_not_exist"
    assert not os.path.isdir(no_dir)
    loader = TrackLoader(workers=1)
    with pytest.raises(ParameterError, match=f"Not a directory: {os.path.abspath(no_dir)}"):
        loader.load_tracks(no_dir)


def test_gpx_dir_no_files(tmp_path_factory: pytest.TempPathFactory) -> None:
    """Temporary gpx directory - empty"""
    empty_dir = tmp_path_factory.mktemp("data")
    assert len(os.listdir(empty_dir)) == 0
    loader = TrackLoader(workers=1)
    loader.load_tracks(str(empty_dir))


def test_gpx_dir_with_files(gpx_dir_with_tracks: Path) -> None:
    """Temporary gpx directory - with files"""
    # 3 files exist
    assert len(list(gpx_dir_with_tracks.iterdir())) == 4
    # 2 gpx files are loaded
    loader = TrackLoader(workers=1)
    loader.set_min_length(500 * Units().meter)
    assert len(loader.load_tracks(str(gpx_dir_with_tracks))) == 3


def test_gpx_dir_with_files_filter_year(gpx_dir_with_tracks: Path) -> None:
    """Temporary gpx directory - with files, filter year"""
    # 3 files exist
    assert len(list(gpx_dir_with_tracks.iterdir())) == 4
    # 2 gpx files are loaded
    loader = TrackLoader(workers=1)
    loader.set_min_length(500 * Units().meter)
    assert len(loader.load_tracks(str(gpx_dir_with_tracks))) == 3
    year_range = YearRange()
    year_range.parse("2022")
    loader.year_range = year_range
    assert len(loader.load_tracks(str(gpx_dir_with_tracks))) == 1
    year_range.parse("2020")
    loader.year_range = year_range
    assert len(loader.load_tracks(str(gpx_dir_with_tracks))) == 0


def test_gpx_dir_with_files_filter_length(gpx_dir_with_tracks: Path) -> None:
    """Temporary gpx directory - with files, filter length"""
    # 3 files exist
    assert len(list(gpx_dir_with_tracks.iterdir())) == 4
    # 2 gpx files are loaded
    loader = TrackLoader(workers=1)
    # default min_length is 1.0km
    assert len(loader.load_tracks(str(gpx_dir_with_tracks))) == 1
    loader.set_min_length(500 * Units().meter)
    assert len(loader.load_tracks(str(gpx_dir_with_tracks))) == 3
    loader.set_min_length(5000 * Units().meter)
    assert len(loader.load_tracks(str(gpx_dir_with_tracks))) == 0


def test_gpx_dir_with_files_filter_activity(gpx_dir_with_tracks: Path) -> None:
    """Temporary gpx directory - with files, filter activity"""
    # 3 files exist
    assert len(list(gpx_dir_with_tracks.iterdir())) == 4
    # 2 gpx files are loaded
    loader = TrackLoader(workers=1)
    loader.set_min_length(500 * Units().meter)
    assert len(loader.load_tracks(str(gpx_dir_with_tracks))) == 3
    loader.set_activity("Hike")
    assert len(loader.load_tracks(str(gpx_dir_with_tracks))) == 1
    loader.set_activity("Walk")
    assert len(loader.load_tracks(str(gpx_dir_with_tracks))) == 1
    loader.set_activity("Bike")
    assert len(loader.load_tracks(str(gpx_dir_with_tracks))) == 0


def test_gpx_dir_with_files_two_workers(gpx_dir_with_tracks: Path) -> None:
    """Temporary gpx directory - with files, two workers"""
    loader = TrackLoader(workers=2)
    loader.set_min_length(500 * Units().meter)
    assert len(loader.load_tracks(str(gpx_dir_with_tracks))) == 3


def test_gpx_dir_with_files_with_cache_dir(gpx_dir_with_tracks: Path, tmp_path_factory: pytest.TempPathFactory) -> None:
    """Temporary gpx directory - with files, with cache"""
    loader = TrackLoader(workers=1)
    loader.set_min_length(500 * Units().meter)
    cache_dir = tmp_path_factory.mktemp("cache")
    loader.set_cache_dir(str(cache_dir))
    assert len(loader.load_tracks(str(gpx_dir_with_tracks))) == 3
    # second run to activate cache
    assert len(loader.load_tracks(str(gpx_dir_with_tracks))) == 3
    # third run with clear cache
    loader.clear_cache()
    assert len(loader.load_tracks(str(gpx_dir_with_tracks))) == 3
