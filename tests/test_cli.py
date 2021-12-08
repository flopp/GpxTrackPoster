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

# from gpxtrackposter.year_range import YearRange


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

    @patch("gpxtrackposter.track_loader.Track", autospec=True)
    @patch("gpxtrackposter.poster.Poster", autospec=True)
    @pytest.mark.skip
    def test_setup_poster_returns_instance_of_poster_with_default_size(
        self, mock_poster: MagicMock, mock_track: MagicMock
    ) -> None:
        """Test setup of poster with default values from argparser"""
        args = self.get_default_values()
        mock_poster.set_tracks.return_value = None
        poster = setup_poster(mock_poster, [mock_track], args)
        self.assertTrue(poster)
        self.assertIsInstance(poster, Poster)
        # default height and width of poster
        self.assertEqual(300, poster.height)
        self.assertEqual(200, poster.width)

    @patch("gpxtrackposter.track_loader.Track", autospec=True)
    @pytest.mark.skip
    def test_setup_poster_type_github_returns_instance_of_poster_with_modified_height(
        self, mock_track: MagicMock
    ) -> None:
        """Test setup of poster with type github"""
        args = TestCase.get_default_values()
        args.type = "github"
        year_count = 3
        mock_track_1 = mock_track.return_value
        mock_track_1.length.return_value = 1 * Units().km
        mock_track_1.start_time.return_value = datetime.datetime(year=2016, month=1, day=1, hour=1, minute=1, second=1)
        mock_track_1.end_time.return_value = datetime.datetime(year=2016, month=1, day=1, hour=2, minute=2, second=2)
        mock_track_1.year = 2016
        mock_track_2 = mock_track.return_value
        mock_track_2.length.return_value = 2 * Units().km
        mock_track_2.start_time.return_value = datetime.datetime(year=2018, month=1, day=1, hour=1, minute=1, second=1)
        mock_track_2.end_time.return_value = datetime.datetime(year=2018, month=1, day=1, hour=2, minute=2, second=2)
        mock_track_2.year = 2018
        poster = setup_poster(Poster(), [mock_track, mock_track_2], args)
        # return
        self.assertTrue(poster)
        self.assertIsInstance(poster, Poster)
        self.assertEqual(poster.years.from_year, 2016)
        self.assertEqual(year_count, poster.years.count())
        # modified height of poster
        self.assertEqual(55 + year_count * 43, poster.height)
        self.assertEqual(200, poster.width)

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


@pytest.fixture(name="mock_track_instance")
def fixture_mock_track_instance(mocker: MockerFixture) -> MagicMock:
    mock_track_class = mocker.patch("gpxtrackposter.track_loader.Track")
    instance = mock_track_class.return_value
    instance.length.return_value = 1 * Units().km
    instance.start_time.return_value = datetime.datetime.now()
    instance.end_time.return_value = datetime.datetime.now()
    return instance


if __name__ == "__main__":
    unittest.main()
