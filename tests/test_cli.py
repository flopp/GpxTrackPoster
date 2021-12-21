"""
Several tests for entry point cli.py
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import argparse
import datetime
import logging
import os
import unittest
from unittest.mock import MagicMock, patch

import pytest
from pytest_mock import MockerFixture

from gpxtrackposter.cli import parse_args, create_parser, setup_logging, setup_loader, setup_poster
from gpxtrackposter.exceptions import ParameterError
from gpxtrackposter.poster import Poster
from gpxtrackposter.track_loader import TrackLoader
from gpxtrackposter.units import Units


class TestCase(unittest.TestCase):
    """
    Test class for entry point cli.py
    """

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            os.remove("poster.svg")
            os.remove("logger.log")
        except FileNotFoundError:
            pass

    def test_create_parser_without_args_sets_default_values(self) -> None:
        parser = create_parser()
        parsed = parse_args(parser, [])
        default_values = self.get_default_values()
        for value in vars(default_values):
            if getattr(default_values, value) is None:
                self.assertIsNone(getattr(parsed, value))
            else:
                self.assertIsNotNone(getattr(parsed, value))
                self.assertEqual(getattr(default_values, value), getattr(parsed, value))

    def test_setup_logging_returns_instance_of_logger(self) -> None:
        """Test setup of logging"""
        logger = setup_logging()
        self.assertTrue(logger)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logging.ERROR, logger.getEffectiveLevel())

    def test_setup_logging_verbose_sets_logger_level_info(self) -> None:
        """Test setup of logging"""
        logger = setup_logging(verbose=True)
        self.assertTrue(logger)
        self.assertEqual(logging.INFO, logger.getEffectiveLevel())

    def test_setup_logging_logfile_sets_file_handler(self) -> None:
        """Test setup of logging"""
        logger = setup_logging(logfile="logger.log")
        self.assertTrue(logger)
        handler_names = [handler.__class__.__name__ for handler in logger.handlers]
        self.assertIn("FileHandler", handler_names)

    def test_setup_loader_returns_instance_of_track_loader(self) -> None:
        """Test setup of track loader"""
        args = self.get_default_values()
        loader = setup_loader(args)
        self.assertTrue(loader)
        self.assertIsInstance(loader, TrackLoader)

    def test_setup_loader_clears_cache(self) -> None:
        """Test cache clearing is called"""
        args = self.get_default_values()
        args.clear_cache = True
        loader = setup_loader(args)
        self.assertTrue(loader)
        self.assertIsInstance(loader, TrackLoader)
        with patch("gpxtrackposter.track_loader.TrackLoader.clear_cache") as patched_function:
            loader.clear_cache()
        patched_function.assert_called()

    def test_setup_loader_with_invalid_year_raises_parameter_error(self) -> None:
        """Test Exception is raised with invalid year"""
        args = self.get_default_values()
        args.year = "202x"
        with self.assertRaises(ParameterError):
            setup_loader(args)

    @staticmethod
    def get_default_values() -> argparse.Namespace:
        """Return default values as argparse.Namespace"""
        args = argparse.Namespace(
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
        return args


@pytest.fixture(name="mock_track_instance_1")
def fixture_mock_track_instance_1(mocker: MockerFixture) -> MagicMock:
    mock_track_class = mocker.patch("gpxtrackposter.track_loader.Track")
    instance = mock_track_class.return_value
    instance.length.return_value = 1 * Units().km
    instance.start_time.return_value = datetime.datetime.now()
    instance.end_time.return_value = datetime.datetime.now()
    return instance


@pytest.fixture(name="mock_track_instance_2")
def fixture_mock_track_instance_2(mocker: MockerFixture) -> MagicMock:
    mock_track_class = mocker.patch("gpxtrackposter.track_loader.Track")
    instance = mock_track_class.return_value
    instance.length.return_value = 2 * Units().km
    instance.start_time.return_value = datetime.datetime.now()
    instance.end_time.return_value = datetime.datetime.now()
    return instance


def test_setup_poster_returns_instance_of_poster_with_default_size(
    mocker: MockerFixture, mock_track_instance_1: MagicMock, mock_track_instance_2: MagicMock
) -> None:
    """Test setup of poster with default values from argparser"""
    mocker.patch("gpxtrackposter.poster.Poster.draw", return_value=None)
    args = TestCase.get_default_values()
    poster = setup_poster([mock_track_instance_1, mock_track_instance_2], args)
    assert poster
    assert isinstance(poster, Poster)
    # default height and width of poster
    assert poster.height == 300
    assert poster.width == 200


def test_setup_poster_type_github_returns_instance_of_poster_with_modified_height(
    mocker: MockerFixture, mock_track_instance_1: MagicMock, mock_track_instance_2: MagicMock
) -> None:
    """Test setup of poster with type github"""
    mocker.patch("gpxtrackposter.poster.Poster.draw", return_value=None)
    args = TestCase.get_default_values()
    args.type = "github"
    year_count = 3
    mock_track_instance_1.length.return_value = 1 * Units().km
    mock_track_instance_1.start_time.return_value = datetime.datetime(
        year=2016, month=1, day=1, hour=1, minute=1, second=1
    )
    mock_track_instance_1.end_time.return_value = datetime.datetime(
        year=2016, month=1, day=1, hour=2, minute=2, second=2
    )
    mock_track_instance_1.year = 2016
    mock_track_instance_2.length.return_value = 2 * Units().km
    mock_track_instance_2.start_time.return_value = datetime.datetime(
        year=2018, month=1, day=1, hour=1, minute=1, second=1
    )
    mock_track_instance_2.end_time.return_value = datetime.datetime(
        year=2018, month=1, day=1, hour=2, minute=2, second=2
    )
    mock_track_instance_2.year = 2018
    poster = setup_poster([mock_track_instance_1, mock_track_instance_2], args)

    assert poster
    assert isinstance(poster, Poster)
    # assert years
    assert poster.years.from_year == 2016
    assert poster.years.to_year == 2018
    assert year_count == poster.years.count()
    # modified height of poster
    assert poster.height == 55 + year_count * 43
    assert poster.width == 200


if __name__ == "__main__":
    unittest.main()
