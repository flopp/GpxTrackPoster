#!/usr/bin/env python

# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
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
    p = poster.Poster()
    drawers = {"grid": grid_drawer.GridDrawer(p),
               "calendar": calendar_drawer.CalendarDrawer(p),
               "heatmap": heatmap_drawer.HeatmapDrawer(p),
               "circular": circular_drawer.CircularDrawer(p)}

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--gpx-dir', dest='gpx_dir', metavar='DIR', type=str, default='.',
                             help='Directory containing GPX files (default: current directory).')
    args_parser.add_argument('--output', metavar='FILE', type=str, default='poster.svg',
                             help='Name of generated SVG image file (default: "poster.svg").')
    args_parser.add_argument('--year', metavar='YEAR', type=str, default='all',
                             help='Filter tracks by year; "NUM", "NUM-NUM", "all" (default: all years)')
    args_parser.add_argument('--title', metavar='TITLE', type=str, default="My Tracks",
                             help='Title to display (default: "My Tracks").')
    args_parser.add_argument('--athlete', metavar='NAME', type=str, default="John Doe",
                             help='Athlete name to display (default: "John Doe").')
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
    args = args_parser.parse_args()

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
    p.set_tracks(tracks)
    p.draw(drawers[args.type], args.output)


if __name__ == '__main__':
    try:
        main()
    except PosterError as e:
        print(e)
        sys.exit(1)
