"""
Several tests for entry point cli.py
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import argparse
import logging
import os
import unittest
from unittest.mock import patch

from gpxtrackposter.cli import parse_args, create_parser, setup_logging, setup_loader, setup_poster
from gpxtrackposter.exceptions import ParameterError
from gpxtrackposter.poster import Poster
from gpxtrackposter.track_loader import TrackLoader


class TestCase(unittest.TestCase):
    """
    Test class for entry point cli.py
    """

    @classmethod
    def tearDownClass(cls) -> None:
        try:
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
                self.assertEqual(getattr(parsed, value), getattr(default_values, value))

    def test_setup_logging_returns_instance_of_logger(self) -> None:
        """Test setup of logging"""
        logger = setup_logging()
        self.assertTrue(logger)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.getEffectiveLevel(), logging.ERROR)

    def test_setup_logging_verbose_sets_logger_level_info(self) -> None:
        """Test setup of logging"""
        logger = setup_logging(verbose=True)
        self.assertTrue(logger)
        self.assertEqual(logger.getEffectiveLevel(), logging.INFO)

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

    def test_setup_poster_returns_instance_of_poster(self) -> None:
        """Test setup of poster"""
        with patch("gpxtrackposter.track_loader.Track") as patch_track_instance:
            instance_track = patch_track_instance.return_value
            instance_track.from_year.return_value = 2016
            instance_track.to_year.return_value = 2018
            with patch("gpxtrackposter.poster.Poster") as patch_poster:
                instance_poster = patch_poster.return_value
                instance_poster.set_tracks.return_value = None
                poster = setup_poster(instance_poster, [instance_track], self.get_default_values())
            self.assertTrue(poster)
            self.assertIsInstance(poster, Poster)

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


if __name__ == "__main__":
    unittest.main()
