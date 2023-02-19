# Copyright 2020-2022 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import datetime
import json
from pathlib import Path
from typing import Union, Dict, List
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from gpxtrackposter.track_loader import TrackLoader
from gpxtrackposter.units import Units


def mock_activity(mocker: MockerFixture, activity_type: Union[str, list]) -> MagicMock:
    activity = mocker.MagicMock()
    activity.type = activity_type
    return activity


@pytest.fixture(name="mock_run_activity")
def fixture_mock_run_activity(mocker: MockerFixture) -> MagicMock:
    return mock_activity(mocker, "Run")


@pytest.fixture(name="mock_walk_activity")
def fixture_mock_walk_activity(mocker: MockerFixture) -> MagicMock:
    return mock_activity(mocker, "Walk")


@pytest.fixture(name="mock_hike_activity")
def fixture_mock_hike_activity(mocker: MockerFixture) -> MagicMock:
    return mock_activity(mocker, "Hike")


def strava_config(tmp_path: Path, activity_type: Union[str, List[str], None] = None) -> str:
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
    return strava_config(tmp_path)


@pytest.fixture(name="strava_config_with_run_type_filter")
def fixture_strava_config_with_run_type_filter(tmp_path: Path) -> str:
    return strava_config(tmp_path, "Run")


@pytest.fixture(name="strava_config_with_walk_hike_type_filter")
def fixture_strava_config_with_walk_hike_type_filter(tmp_path: Path) -> str:
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


@pytest.fixture(name="mock_track_instance")
def fixture_mock_track_instance(mocker: MockerFixture) -> MagicMock:
    mock_track_class = mocker.patch("gpxtrackposter.track_loader.Track")
    instance = mock_track_class.return_value
    instance.length.return_value = 1 * Units().km
    instance.start_time.return_value = datetime.datetime.now()
    instance.end_time.return_value = datetime.datetime.now()
    return instance


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
