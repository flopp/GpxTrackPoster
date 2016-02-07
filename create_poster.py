#!/usr/bin/env python

import argparse
import datetime
import appdirs
import os
from src import track_loader
from src import poster
from src import grid_drawer
from src import calendar_drawer
from src import heatmap_drawer


__app_name__ = "create_poster"
__app_author__ = "flopp.net"


def main():
    generators = {"grid": grid_drawer.TracksDrawer(),
                  "calendar": calendar_drawer.TracksDrawer(),
                  "heatmap": heatmap_drawer.TracksDrawer()}

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--gpx-dir', dest='gpx_dir', metavar='DIR', type=str, default='.',
                             help='Directory containing GPX files (default: current directory).')
    args_parser.add_argument('--output', metavar='FILE', type=str, default='poster.svg',
                             help='Name of generated SVG image file (default: "poster.svg").')
    args_parser.add_argument('--year', metavar='YEAR', type=int, default=datetime.date.today().year - 1,
                             help='Filter tracks by year (default: past year)')
    args_parser.add_argument('--title', metavar='TITLE', type=str, default="My Tracks",
                             help='Title to display (default: "My Tracks").')
    args_parser.add_argument('--athlete', metavar='NAME', type=str, default="John Doe",
                             help='Athlete name to display (default: "John Doe").')
    args_parser.add_argument('--special', metavar='FILE', action='append', default=[],
                             help='Mark track file from the GPX directory as special; use multiple times to mark multiple tracks.')
    args_parser.add_argument('--type', metavar='TYPE', default='grid', choices=generators.keys(),
                             help='Type of poster to create (default: "grid", available: "{}").'.format('", "'.join(generators.keys())))
    args_parser.add_argument('--background-color', dest='background_color', metavar='COLOR', type=str,
                             default='#222222', help='Background color of poster (default: "#222222").')
    args_parser.add_argument('--track-color', dest='track_color', metavar='COLOR', type=str, default='#4DD2FF',
                             help='Color of tracks (default: "#4DD2FF").')
    args_parser.add_argument('--text-color', dest='text_color', metavar='COLOR', type=str, default='#FFFFFF',
                             help='Color of text (default: "#FFFFFF").')
    args_parser.add_argument('--special-color', dest='special_color', metavar='COLOR', default='#FFFF00',
                             help='Special track color (default: "#FFFF00").')
    args_parser.add_argument('--clear-cache', dest='clear_cache', action='store_true', help='Clear the track cache.')
    args = args_parser.parse_args()

    loader = track_loader.TrackLoader()
    loader.cache_dir = os.path.join(appdirs.user_cache_dir(__app_name__, __app_author__), "tracks")
    loader.year = args.year
    loader.special_file_names = args.special
    if args.clear_cache:
        loader.clear_cache()
    tracks = loader.load_tracks(args.gpx_dir)
    if not tracks:
        raise Exception('No tracks found.')

    print("Creating poster of type '{}' and storing it in file '{}'...".format(args.type, args.output))
    p = poster.Poster(generators[args.type])
    p.year = args.year
    p.athlete = args.athlete
    p.title = args.title
    p.colors = {'background': args.background_color,
                'track': args.track_color,
                'special': args.special_color,
                'text': args.text_color}
    p.tracks = tracks
    p.draw(args.output)


if __name__ == '__main__':
    main()
