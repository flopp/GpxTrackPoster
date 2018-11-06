#!/usr/bin/env python
"""Create a variety of poster-style visualizations from GPX data

usage: create_poster.py [-h] [--gpx-dir DIR] [--output FILE] [--year YEAR]
                        [--title TITLE] [--athlete NAME] [--special FILE]
                        [--type TYPE] [--background-color COLOR]
                        [--track-color COLOR] [--track-color2 COLOR]
                        [--text-color COLOR] [--special-color COLOR]
                        [--special-color2 COLOR] [--units UNITS]
                        [--clear-cache] [--verbose] [--logfile FILE]
                        [--heatmap-center LAT,LNG]
                        [--heatmap-radius RADIUS_KM] [--circular-rings]
                        [--circular-ring-color COLOR]
                        [--json-dir DIR]  [--stat-label LABEL] [--stat-num NUMBER]
                        [--stat-total KM] [--stat-min KM] [--stat-max KM]

optional arguments:
  -h, --help            show this help message and exit
  --gpx-dir DIR         Directory containing GPX files (default: current
                        directory).
  --json-dir DIR        Directory containing JSON files (default: none).
  --output FILE         Name of generated SVG image file (default:
                        "poster.svg").
  --year YEAR           Filter tracks by year; "NUM", "NUM-NUM", "all"
                        (default: all years)
  --title TITLE         Title to display (default: "My Tracks").
  --athlete NAME        Athlete name to display (default: "John Doe").
  --special FILE        Mark track file from the GPX directory as special; use
                        multiple times to mark multiple tracks.
  --type TYPE           Type of poster to create (default: "grid", available:
                        "grid", "calendar", "heatmap", "circular").
  --background-color COLOR
                        Background color of poster (default: "#222222").
  --track-color COLOR   Color of tracks (default: "#4DD2FF").
  --track-color2 COLOR  Secondary color of tracks (default: none).
  --text-color COLOR    Color of text (default: "#FFFFFF").
  --special-color COLOR
                        Special track color (default: "#FFFF00").
  --special-color2 COLOR
                        Secondary color of special tracks (default: none).
  --units UNITS         Distance units; "metric", "imperial" (default:
                        "metric").
  --clear-cache         Clear the track cache.
  --verbose             Verbose logging.
  --logfile FILE
  --stat-label LABEL    Label for number of activities (default: "Runs").
  --stat-num NUMBER     Number of activities (default: automatically calculated).
  --stat-total KM       Total distance (default: automatically calculated).
  --stat-min KM         Minimal distance (default: automatically calculated).
  --stat-max KM         Maximale distance (default: automatically calculated).

Heatmap Type Options:
  --heatmap-center LAT,LNG
                        Center of the heatmap (default: automatic).
  --heatmap-radius RADIUS_KM
                        Scale the heatmap such that at least a circle with
                        radius=RADIUS_KM is visible (default: automatic).

Circular Type Options:
  --circular-rings      Draw distance rings.
  --circular-ring-color COLOR
                        Color of distance rings.

"""
# Copyright 2016-2018 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import argparse
import appdirs
import logging
import os
import sys
from gpxtrackposter import poster, track_loader
from gpxtrackposter import grid_drawer, calendar_drawer, circular_drawer, heatmap_drawer
from gpxtrackposter.exceptions import ParameterError, PosterError

__app_name__ = "create_poster"
__app_author__ = "flopp.net"


def main():
    """Handle command line arguments and call other modules as needed."""

    p = poster.Poster()
    drawers = {"grid": grid_drawer.GridDrawer(p),
               "calendar": calendar_drawer.CalendarDrawer(p),
               "heatmap": heatmap_drawer.HeatmapDrawer(p),
               "circular": circular_drawer.CircularDrawer(p)}

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--gpx-dir', dest='gpx_dir', metavar='DIR', type=str, default='.',
                             help='Directory containing GPX files (default: current directory).')
    args_parser.add_argument('--json-dir', dest='json_dir', metavar='DIR', type=str, default='',
                             help='Directory containing JSON files (default: none).')
    args_parser.add_argument('--output', metavar='FILE', type=str, default='poster.svg',
                             help='Name of generated SVG image file (default: "poster.svg").')
    args_parser.add_argument('--year', metavar='YEAR', type=str, default='all',
                             help='Filter tracks by year; "NUM", "NUM-NUM", "all" (default: all years)')
    args_parser.add_argument('--title', metavar='TITLE', type=str, default="",
                             help='Title to display (default: "").')
    args_parser.add_argument('--athlete', metavar='NAME', type=str, default="",
                             help='Athlete name to display (default: "").')
    args_parser.add_argument('--special', metavar='FILE', action='append', default=[],
                             help='Mark track file from the GPX directory as special; use multiple times to mark '
                                  'multiple tracks.')
    args_parser.add_argument('--type', metavar='TYPE', default='grid', choices=drawers.keys(),
                             help='Type of poster to create (default: "grid", available: "{}").'
                             .format('", "'.join(drawers.keys())))
    args_parser.add_argument('--background-color', dest='background_color', metavar='COLOR', type=str,
                             default='#222222', help='Background color of poster (default: "#222222").')
    args_parser.add_argument('--track-color', dest='track_color', metavar='COLOR', type=str, default='#4DD2FF',
                             help='Color of tracks (default: "#4DD2FF").')
    args_parser.add_argument('--track-color2', dest='track_color2', metavar='COLOR', type=str,
                             help='Secondary color of tracks (default: none).')
    args_parser.add_argument('--text-color', dest='text_color', metavar='COLOR', type=str, default='#FFFFFF',
                             help='Color of text (default: "#FFFFFF").')
    args_parser.add_argument('--special-color', dest='special_color', metavar='COLOR', default='#FFFF00',
                             help='Special track color (default: "#FFFF00").')
    args_parser.add_argument('--special-color2', dest='special_color2', metavar='COLOR',
                             help='Secondary color of special tracks (default: none).')
    args_parser.add_argument('--units', dest='units', metavar='UNITS', type=str, choices=['metric', 'imperial'],
                             default='metric', help='Distance units; "metric", "imperial" (default: "metric").')
    args_parser.add_argument('--clear-cache', dest='clear_cache', action='store_true', help='Clear the track cache.')
    args_parser.add_argument('--verbose', dest='verbose', action='store_true', help='Verbose logging.')
    args_parser.add_argument('--logfile', dest='logfile', metavar='FILE', type=str)
    args_parser.add_argument('--stat-label', dest='stat_label', metavar='LABEL', type=str, default="Activities",
                             help='Statistics: label for number of activities')
    args_parser.add_argument('--stat-num', dest='stat_num', metavar='NUMBER', type=int, default=0,
                             help='Statistics: number of activities')
    args_parser.add_argument('--stat-total', dest='stat_total', metavar='KM', type=float, default=0.0,
                             help='Statistics: total distance')
    args_parser.add_argument('--stat-min', dest='stat_min', metavar='KM', type=float, default=0.0,
                             help='Statistics: minimal distance')
    args_parser.add_argument('--stat-max', dest='stat_max', metavar='KM', type=float, default=0.0,
                             help='Statistics: maximal distance')

    for _, drawer in drawers.items():
        drawer.create_args(args_parser)

    args = args_parser.parse_args()

    for _, drawer in drawers.items():
        drawer.fetch_args(args)

    log = logging.getLogger('gpxtrackposter')
    log.setLevel(logging.INFO if args.verbose else logging.ERROR)
    if args.logfile:
        handler = logging.FileHandler(args.logfile)
        log.addHandler(handler)

    loader = track_loader.TrackLoader()
    loader.cache_dir = os.path.join(appdirs.user_cache_dir(__app_name__, __app_author__), "tracks")
    if not loader.year_range.parse(args.year):
        raise ParameterError('Bad year range: {}.'.format(args.year))

    loader.special_file_names = args.special
    if args.clear_cache:
        print('Clearing cache...')
        loader.clear_cache()

    if args.json_dir:
    	tracks = loader.load_tracks(args.json_dir, True)
    else:
    	tracks = loader.load_tracks(args.gpx_dir)
    if not tracks:
        if not args.clear_cache:
            print('No tracks found.')
        return

    print("Creating poster of type '{}' with {} tracks and storing it in file '{}'...".format(args.type, len(tracks),
                                                                                              args.output))
    p.athlete = args.athlete
    p.title = args.title
    p.colors = {'background': args.background_color,
                'track': args.track_color,
                'track2': args.track_color2 if args.track_color2 is not None else args.track_color,
                'special': args.special_color,
                'special2': args.special_color2 if args.special_color2 is not None else args.special_color,
                'text': args.text_color}
    p.units = args.units
    p.statistics = {'label': args.stat_label,
                    'num': args.stat_num,
                    'total': args.stat_total,
                    'min': args.stat_min,
                    'max': args.stat_max}
    p.set_tracks(tracks)
    p.draw(drawers[args.type], args.output)


if __name__ == '__main__':
    try:
        main()
    except PosterError as e:
        print(e)
        sys.exit(1)
