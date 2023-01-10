"""
Several tests for entry point cli.py
"""
# Copyright 2021-2022 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import argparse
import datetime
import logging
from unittest.mock import MagicMock, patch

import pytest
from pytest_mock import MockerFixture

from gpxtrackposter.cli import parse_args, create_parser, setup_logging, setup_loader, setup_poster
from gpxtrackposter.exceptions import ParameterError
from gpxtrackposter.poster import Poster
from gpxtrackposter.track_loader import TrackLoader
from gpxtrackposter.units import Units


def test_create_parser_without_args_sets_default_values(default_values: argparse.Namespace) -> None:
    parser = create_parser()
    parsed = parse_args(parser, [])
    for value in vars(default_values):
        if getattr(default_values, value) is None:
            assert getattr(parsed, value) is None
        else:
            assert getattr(parsed, value) is not None
            assert getattr(default_values, value) == getattr(parsed, value)


def test_setup_logging_returns_instance_of_logger() -> None:
    """Test setup of logging"""
    logger = setup_logging()
    assert logger
    assert isinstance(logger, logging.Logger)
    assert logging.ERROR == logger.getEffectiveLevel()


def test_setup_logging_verbose_sets_logger_level_info() -> None:
    """Test setup of logging"""
    logger = setup_logging(verbose=True)
    assert logger
    assert logging.INFO == logger.getEffectiveLevel()


def test_setup_logging_logfile_sets_file_handler() -> None:
    """Test setup of logging"""
    logger = setup_logging(logfile="logger.log")
    assert logger
    handler_names = [handler.__class__.__name__ for handler in logger.handlers]
    assert "FileHandler" in handler_names


def test_setup_loader_returns_instance_of_track_loader(default_values: argparse.Namespace) -> None:
    """Test setup of track loader"""
    loader = setup_loader(default_values)
    assert loader
    assert isinstance(loader, TrackLoader)


def test_setup_loader_clears_cache(default_values: argparse.Namespace) -> None:
    """Test cache clearing is called"""
    default_values.clear_cache = True
    loader = setup_loader(default_values)
    assert loader
    assert isinstance(loader, TrackLoader)
    with patch("gpxtrackposter.track_loader.TrackLoader.clear_cache") as patched_function:
        loader.clear_cache()
    patched_function.assert_called()


def test_setup_loader_with_invalid_year_raises_parameter_error(default_values: argparse.Namespace) -> None:
    """Test Exception is raised with invalid year"""
    default_values.year = "202x"
    with pytest.raises(ParameterError):
        setup_loader(default_values)


def test_setup_poster_returns_instance_of_poster_with_default_size(
    mocker: MockerFixture,
    mock_track_instance_berlin_paris: MagicMock,
    mock_track_instance_amsterdam_paris: MagicMock,
    default_values: argparse.Namespace,
) -> None:
    """Test setup of poster with default values from argparser"""
    mocker.patch("gpxtrackposter.poster.Poster.draw", return_value=None)
    poster = setup_poster([mock_track_instance_berlin_paris, mock_track_instance_amsterdam_paris], default_values)
    assert poster
    assert isinstance(poster, Poster)
    # default height and width of poster
    assert poster.height == 300
    assert poster.width == 200


def test_setup_poster_type_github_returns_instance_of_poster_with_modified_height(
    mocker: MockerFixture,
    mock_track_instance_berlin_paris: MagicMock,
    mock_track_instance_amsterdam_paris: MagicMock,
    default_values: argparse.Namespace,
) -> None:
    """Test setup of poster with type GitHub"""
    mocker.patch("gpxtrackposter.poster.Poster.draw", return_value=None)
    default_values.type = "github"
    year_count = 3
    mock_track_instance_berlin_paris.length.return_value = 1 * Units().km
    mock_track_instance_berlin_paris.start_time.return_value = datetime.datetime(
        year=2016, month=1, day=1, hour=1, minute=1, second=1
    )
    mock_track_instance_berlin_paris.end_time.return_value = datetime.datetime(
        year=2016, month=1, day=1, hour=2, minute=2, second=2
    )
    mock_track_instance_berlin_paris.year = 2016
    mock_track_instance_amsterdam_paris.length.return_value = 2 * Units().km
    mock_track_instance_amsterdam_paris.start_time.return_value = datetime.datetime(
        year=2018, month=1, day=1, hour=1, minute=1, second=1
    )
    mock_track_instance_amsterdam_paris.end_time.return_value = datetime.datetime(
        year=2018, month=1, day=1, hour=2, minute=2, second=2
    )
    mock_track_instance_amsterdam_paris.year = 2018
    poster = setup_poster([mock_track_instance_berlin_paris, mock_track_instance_amsterdam_paris], default_values)

    assert poster
    assert isinstance(poster, Poster)
    # assert years
    assert poster.years.from_year == 2016
    assert poster.years.to_year == 2018
    assert year_count == poster.years.count()
    # modified height of poster
    assert poster.height == 55 + year_count * 43
    assert poster.width == 200
