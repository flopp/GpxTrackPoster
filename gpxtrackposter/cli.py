#!/usr/bin/env python
"""
Entry point - cli.py
"""
# Copyright 2016-2023 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import argparse
import logging
import os
import sys
from typing import List

import appdirs  # type: ignore

from gpxtrackposter import github_drawer, calendar_drawer
from gpxtrackposter import grid_drawer, circular_drawer, heatmap_drawer
from gpxtrackposter import poster, track_loader
from gpxtrackposter.exceptions import ParameterError, PosterError
from gpxtrackposter.units import Units


__app_name__ = "create_poster"
__app_author__ = "flopp.net"

p = poster.Poster()
drawers = {
    "grid": grid_drawer.GridDrawer(p),
    "calendar": calendar_drawer.CalendarDrawer(p),
    "heatmap": heatmap_drawer.HeatmapDrawer(p),
    "circular": circular_drawer.CircularDrawer(p),
    "github": github_drawer.GithubDrawer(p),
}


def main() -> None:
    """Handle command line arguments and call other modules as needed."""

    # create basic args parser
    args_parser = create_parser()

    # add command line options for every single drawer type
    for _, drawer in drawers.items():
        drawer.create_args(args_parser)

    # parse all arguments
    args = parse_args(args_parser, sys.argv[1:])

    # fetch all arguments
    for _, drawer in drawers.items():
        drawer.fetch_args(args)

    # setup logging
    setup_logging(args.verbose, args.logfile)

    # setup loader
    loader = setup_loader(args)

    # setup tracks
    if args.from_strava:
        tracks = loader.load_strava_tracks(args.from_strava)
    else:
        tracks = loader.load_tracks(args.gpx_dir)
    if not tracks:
        if not args.clear_cache:
            print("No tracks found.")
        return

    # setup poster
    setup_poster(tracks, args)


def parse_args(args_parser: argparse.ArgumentParser, args: list) -> argparse.Namespace:
    """Parse arguments"""
    return args_parser.parse_args(args)


def create_parser() -> argparse.ArgumentParser:
    """Add arguments to the parser"""
    args_parser = argparse.ArgumentParser(prog=__app_name__)
    args_parser.add_argument(
        "--gpx-dir",
        dest="gpx_dir",
        metavar="DIR",
        type=str,
        default=".",
        help="Directory containing GPX files (default: current directory).",
    )
    args_parser.add_argument(
        "--output",
        metavar="FILE",
        type=str,
        default="poster.svg",
        help='Name of generated SVG image file (default: "poster.svg").',
    )
    args_parser.add_argument(
        "--language",
        metavar="LANGUAGE",
        type=str,
        default="",
        help="Language (default: english).",
    )
    args_parser.add_argument(
        "--localedir",
        metavar="DIR",
        type=str,
        help="The directory where the translation files can be found (default: the system's locale directory).",
    )
    args_parser.add_argument(
        "--year",
        metavar="YEAR",
        type=str,
        default="all",
        help='Filter tracks by year; "NUM", "NUM-NUM", "all" (default: all years)',
    )
    args_parser.add_argument("--title", metavar="TITLE", type=str, help="Title to display.")
    args_parser.add_argument(
        "--athlete",
        metavar="NAME",
        type=str,
        default="John Doe",
        help='Athlete name to display (default: "John Doe").',
    )
    args_parser.add_argument(
        "--special",
        metavar="FILE",
        action="append",
        default=[],
        help="Mark track file from the GPX directory as special; use multiple times to mark " "multiple tracks.",
    )
    types = '", "'.join(drawers.keys())
    args_parser.add_argument(
        "--type",
        metavar="TYPE",
        default="grid",
        choices=drawers.keys(),
        help=f'Type of poster to create (default: "grid", available: "{types}").',
    )
    args_parser.add_argument(
        "--background-color",
        dest="background_color",
        metavar="COLOR",
        type=str,
        default="#222222",
        help='Background color of poster (default: "#222222").',
    )
    args_parser.add_argument(
        "--track-color",
        dest="track_color",
        metavar="COLOR",
        type=str,
        default="#4DD2FF",
        help='Color of tracks (default: "#4DD2FF").',
    )
    args_parser.add_argument(
        "--track-color2",
        dest="track_color2",
        metavar="COLOR",
        type=str,
        help="Secondary color of tracks (default: none).",
    )
    args_parser.add_argument(
        "--text-color",
        dest="text_color",
        metavar="COLOR",
        type=str,
        default="#FFFFFF",
        help='Color of text (default: "#FFFFFF").',
    )
    args_parser.add_argument(
        "--special-color",
        dest="special_color",
        metavar="COLOR",
        default="#FFFF00",
        help='Special track color (default: "#FFFF00").',
    )
    args_parser.add_argument(
        "--special-color2",
        dest="special_color2",
        metavar="COLOR",
        help="Secondary color of special tracks (default: none).",
    )
    args_parser.add_argument(
        "--units",
        dest="units",
        metavar="UNITS",
        type=str,
        choices=["metric", "imperial"],
        default="metric",
        help='Distance units; "metric", "imperial" (default: "metric").',
    )
    args_parser.add_argument(
        "--clear-cache",
        dest="clear_cache",
        action="store_true",
        help="Clear the track cache.",
    )
    args_parser.add_argument(
        "--workers",
        dest="workers",
        metavar="NUMBER_OF_WORKERS",
        type=int,
        help="Number of parallel track loading workers (default: number of CPU cores)",
    )
    args_parser.add_argument(
        "--from-strava",
        dest="from_strava",
        metavar="FILE",
        type=str,
        help="JSON file containing config used to get activities from strava",
    )
    args_parser.add_argument("--verbose", dest="verbose", action="store_true", help="Verbose logging.")
    args_parser.add_argument("--logfile", dest="logfile", metavar="FILE", type=str)
    args_parser.add_argument(
        "--special-distance",
        dest="special_distance",
        metavar="DISTANCE",
        type=float,
        default=10.0,
        help="Special Distance1 by km and color with the special_color",
    )
    args_parser.add_argument(
        "--special-distance2",
        dest="special_distance2",
        metavar="DISTANCE",
        type=float,
        default=20.0,
        help="Special Distance2 by km and color with the special_color2",
    )
    args_parser.add_argument(
        "--min-distance",
        dest="min_distance",
        metavar="DISTANCE",
        type=float,
        default=1.0,
        help="min distance by km for track filter",
    )
    args_parser.add_argument(
        "--activity-type",
        "--activity",
        dest="activity_type",
        metavar="ACTIVITY_TYPE",
        type=str,
        default="all",
        help="Filter tracks by activity type; e.g. 'running' (default: all activity types)",
    )
    args_parser.add_argument(
        "--with-animation",
        dest="with_animation",
        action="store_true",
        help="add animation to the poster",
    )
    args_parser.add_argument(
        "--animation-time",
        dest="animation_time",
        type=int,
        default=30,
        help="animation duration (default: 30s)",
    )
    return args_parser


def setup_logging(verbose: bool = False, logfile: str = None) -> logging.Logger:
    """Set up logging"""
    log = logging.getLogger("gpxtrackposter")
    log.setLevel(logging.INFO if verbose else logging.ERROR)
    if logfile:
        handler = logging.FileHandler(logfile)
        log.addHandler(handler)
    return log


def setup_loader(args: argparse.Namespace) -> track_loader.TrackLoader:
    """Set up the tracks loader"""
    loader = track_loader.TrackLoader(args.workers)
    loader.set_cache_dir(os.path.join(appdirs.user_cache_dir(__app_name__, __app_author__), "tracks"))
    if not loader.year_range.parse(args.year):
        raise ParameterError(f"Bad year range: {args.year}.")

    loader.special_file_names = args.special
    loader.set_min_length(args.min_distance * Units().km)
    loader.set_activity(args.activity_type)
    if args.clear_cache:
        print("Clearing cache...")
        loader.clear_cache()
    return loader


def setup_poster(tracks: List[track_loader.Track], args: argparse.Namespace) -> poster.Poster:
    """Set up the poster"""
    print(f"Creating poster of type {args.type} with {len(tracks)} tracks and storing it in file {args.output}...")
    pstr = poster.Poster()
    pstr.set_language(args.language, args.localedir)
    pstr.set_athlete(args.athlete)
    pstr.set_title(args.title if args.title else p.translate("MY TRACKS"))
    pstr.set_with_animation(args.with_animation)
    pstr.set_animation_time(args.animation_time)

    pstr.special_distance = {
        "special_distance": args.special_distance * Units().km,
        "special_distance2": args.special_distance2 * Units().km,
    }

    pstr.colors = {
        "background": args.background_color,
        "track": args.track_color,
        "track2": args.track_color2 or args.track_color,
        "special": args.special_color,
        "special2": args.special_color2 or args.special_color,
        "text": args.text_color,
    }
    pstr.units = args.units
    pstr.set_tracks(tracks)
    if args.type == "github":
        pstr.height = 55 + pstr.years.count() * 43
    pstr.draw(drawers[args.type], args.output)
    return pstr


if __name__ == "__main__":
    try:
        main()
    except PosterError as e:
        print(e)
        sys.exit(1)
