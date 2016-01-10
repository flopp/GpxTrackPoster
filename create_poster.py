#!/usr/bin/env python

import argparse
import datetime
import gpxpy
import math
import os
import svgwrite


class Track:
    def __init__(self):
        self.file_name = None
        self.gpx = None
        self.start_time = None
        self.end_time = None
        self.length = 0

    def load_gpx(self, file_name):
        self.file_name = file_name
        file = open(self.file_name, 'r')
        self.gpx = gpxpy.parse(file)
        b = self.gpx.get_time_bounds()
        self.start_time = b[0]
        self.end_time = b[1]
        self.length = self.gpx.length_2d()

    def append(self, other):
        self.end_time = other.end_time
        self.gpx.tracks.extend(other.gpx.tracks)
        self.length += other.length


def list_gpx_files(base_dir):
    base_dir = os.path.abspath(base_dir)
    if not os.path.isdir(base_dir):
        raise Exception("Not a directory: {}".format(base_dir))
    for name in os.listdir(base_dir):
        path_name = os.path.join(base_dir, name)
        if name.endswith(".gpx") and os.path.isfile(path_name):
            yield path_name


def load_tracks(base_dir, year, min_length):
    tracks = []
    file_names = [x for x in list_gpx_files(base_dir)]
    for (index, file_name) in enumerate(file_names):
        print("loading file {}/{}".format(index, len(file_names)))
        try:
            t = Track()
            t.load_gpx(file_name)
            t.gpx.simplify()
            if t.length == 0:
                print("{}: skipping empty track", file_name)
            elif not t.start_time:
                print("{}: skipping track without start time", file_name)
            elif t.start_time.year != year:
                print("{}: skipping track with wrong year {}", file_name, t.start_time.year)
            else:
                tracks.append(t)
        except Exception as e:
            print("{}: error while parsing GPX file; {}", file_name, e)

    # sort tracks by start time
    sorted_tracks = sorted(tracks, key=lambda t: t.start_time)

    # merge tracks that took place within one hour
    merged_tracks = []
    last_end_time = None
    for t in sorted_tracks:
        if last_end_time is None:
            merged_tracks.append(t)
        else:
            dt = (t.start_time - last_end_time).total_seconds()
            if 0 < dt < 3600:
                print("Merging track with previous, due to time distance of {}s.".format(dt))
                merged_tracks[-1].append(t)
            else:
                merged_tracks.append(t)
        last_end_time = t.end_time

    # filter out tracks with length < min_length
    return [t for t in merged_tracks if t.length >= min_length]


def draw_track(track, drawing, x_offset, y_offset, width, height, color):
    b = track.gpx.get_bounds()

    min_lat = b.min_latitude
    cos_lat = math.cos(0.5 * (b.min_latitude + b.max_latitude) * math.pi/180)
    min_lng = cos_lat * b.min_longitude
    d_lat = b.max_latitude - b.min_latitude
    d_lng = cos_lat * (b.max_longitude - b.min_longitude)

    scale = width/d_lng
    if width/height > d_lng/d_lat:
        scale = height/d_lat

    x_offset += 0.5 * width - 0.5 * scale * d_lng
    y_offset += 0.5 * height + 0.5 * scale * d_lat

    lines = []
    for t in track.gpx.tracks:
        for s in t.segments:
            polyline = []
            for p in s.points:
                x = x_offset + scale * (cos_lat*p.longitude - min_lng)
                y = y_offset - scale * (p.latitude - min_lat)
                polyline.append((x, y))
            lines.append(polyline)

    for polyline in lines:
        drawing.add(drawing.polyline(points=polyline, stroke=color, fill='none', stroke_width=0.5, stroke_linejoin='round', stroke_linecap='round'))


def compute_lengths(tracks):
    min_length = -1
    max_length = -1
    total_length = 0
    for t in tracks:
        total_length += t.length
        if min_length < 0 or t.length < min_length:
            min_length = t.length
        if max_length < 0 or t.length > max_length:
            max_length = t.length
    return 0.001*total_length, 0.001*total_length/len(tracks), 0.001*min_length, 0.001*max_length


def compute_grid(count, width, height):
    min_waste = -1
    best_size = -1
    for x in range(1, width):
        s = width/x
        waste = width*height - count*s*s
        if waste < 0:
            continue
        if min_waste < 0 or waste < min_waste:
            min_waste = waste
            best_size = s
    count_x = width/best_size
    count_y = count // count_x
    if count % count_x > 0:
        count_y += 1
    spacing_y = (height - count_y * best_size) / count_y

    return best_size, count_x, count_y, spacing_y


def poster(tracks, title, year, athlete_name, output, colors):
    (total_length, average_length, min_length, max_length) = compute_lengths(tracks)

    w = 200
    h = 300
    d = svgwrite.Drawing(output, ('{}mm'.format(w), '{}mm'.format(h)))
    d.viewbox(0, 0, w, h)
    d.add(d.rect((0, 0), (w, h), fill=colors['background']))

    d.add(d.text(title, insert=(10, 20), fill=colors['text'], style="font-size:12px; font-family:Arial; font-weight:bold;"))
    d.add(d.text("YEAR", insert=(10, h-20), fill=colors['text'], style="font-size:4px; font-family:Arial"))
    d.add(d.text("{}".format(year), insert=(10, h-10), fill=colors['text'], style="font-size:9px; font-family:Arial"))
    d.add(d.text("ATHLETE", insert=(40, h-20), fill=colors['text'], style="font-size:4px; font-family:Arial"))
    d.add(d.text(athlete_name, insert=(40, h-10), fill=colors['text'], style="font-size:9px; font-family:Arial"))
    d.add(d.text("STATISTICS", insert=(120, h-20), fill=colors['text'], style="font-size:4px; font-family:Arial"))
    d.add(d.text("Total: {:.2f} km".format(total_length), insert=(120, h-15), fill=colors['text'], style="font-size:4px; font-family:Arial"))
    d.add(d.text("Average: {:.2f} km".format(average_length), insert=(120, h-10), fill=colors['text'], style="font-size:4px; font-family:Arial"))
    d.add(d.text("Min: {:.2f} km".format(min_length), insert=(160, h-15), fill=colors['text'], style="font-size:4px; font-family:Arial"))
    d.add(d.text("Max: {:.2f} km".format(max_length), insert=(160, h-10), fill=colors['text'], style="font-size:4px; font-family:Arial"))

    tracks_w = w - 20
    tracks_h = h - 30 - 30
    tracks_x = 10
    tracks_y = 30

    (size, count_x, count_y, spacing_y) = compute_grid(len(tracks), tracks_w, tracks_h)
    for (index, track) in enumerate(tracks):
        x = index % count_x
        y = index // count_x
        draw_track(track, d, tracks_x+(0.05 + x)*size, tracks_y+(0.05+y)*size+y*spacing_y, 0.9 * size, 0.9 * size, colors['track'])

    d.save()


def main():
    command_line_parser = argparse.ArgumentParser()
    command_line_parser.add_argument('--gpx-dir', dest='gpx_dir', metavar='DIR', type=str, default='.', help='Directory containing GPX files (default: current directory).')
    command_line_parser.add_argument('--year', metavar='YEAR', type=int, default=datetime.date.today().year-1, help='Filter tracks by year (default: past year)')
    command_line_parser.add_argument('--title', metavar='TITLE', type=str, default="My Tracks", help='Title to display (default: "My Tracks").')
    command_line_parser.add_argument('--athlete', metavar='NAME', type=str, default="John Doe", help='Athlete name to display (default: "John Doe").')
    command_line_parser.add_argument('--background-color', dest='background_color', metavar='COLOR', type=str, default='#222222', help='Background color of poster (default: "#222222").')
    command_line_parser.add_argument('--track-color', dest='track_color', metavar='COLOR', type=str, default='#4DD2FF', help='Color of tracks (default: "#4DD2FF").')
    command_line_parser.add_argument('--text-color', dest='text_color', metavar='COLOR', type=str, default='#FFFFFF', help='Color of text (default: "#FFFFFF").')
    command_line_parser.add_argument('--output', metavar='FILE', type=str, default='poster.svg', help='Name of generated SVG image file (default: "poster.svg").')
    command_line_args = command_line_parser.parse_args()

    tracks = load_tracks(command_line_args.gpx_dir, command_line_args.year, 1000)
    if not tracks:
        raise Exception('No tracks found.')

    colors = {'background': command_line_args.background_color, 'track': command_line_args.track_color, 'text': command_line_args.text_color}
    poster(tracks, command_line_args.title, command_line_args.year, command_line_args.athlete, command_line_args.output, colors)


if __name__ == '__main__':
    main()