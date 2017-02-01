# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from . import utils


class TracksDrawer:
    def __init__(self):
        self.poster = None

    def draw(self, poster, d, w, h, offset_x, offset_y):
        self.poster = poster
        bbox = poster.bbox
        if None != bbox:
            print("heatmap drawer using bbox: {}" . format(bbox))

        xy_polylines = []
        xy_polylines_special = []
        for track in self.poster.tracks:
            track_xy = []
            for polyline in track.polylines:
                track_xy.append([utils.latlng2xy(lat, lng) for (lat, lng) in polyline])
            xy_polylines.extend(track_xy)
            if track.special:
                xy_polylines_special.extend(track_xy)

        print("bounds xy_polylines: bbox={}" . format(utils.compute_bounds_xy(xy_polylines)))
        print("bounds xy_polylines_special: bbox={}" . format(utils.compute_bounds_xy(xy_polylines_special)))
        # FIXME: do we need to handle special tracks?

        if None == bbox:
            (min_x, min_y, max_x, max_y) = utils.compute_bounds_xy(xy_polylines)
        else:
            (min_x, min_y) = utils.latlng2xy(bbox[0], bbox[3])
            (max_x, max_y) = utils.latlng2xy(bbox[2], bbox[1])

        d_x = max_x - min_x
        d_y = max_y - min_y

        # compute scale
        scale = w/d_x if w/h <= d_x/d_y else h/d_y

        # compute offsets such that projected track is centered in its rect
        offset_x += 0.5 * w - 0.5 * scale * d_x
        offset_y += 0.5 * h - 0.5 * scale * d_y

        scaled_lines = []
        for line in xy_polylines:
            scaled_line = []
            for (x, y) in line:
                scaled_x = offset_x + scale * (x - min_x)
                scaled_y = offset_y + scale * (y - min_y)
                scaled_line.append((scaled_x, scaled_y))
            scaled_lines.append(scaled_line)
        scaled_lines_special = []
        for line in xy_polylines_special:
            scaled_line = []
            for (x, y) in line:
                scaled_x = offset_x + scale * (x - min_x)
                scaled_y = offset_y + scale * (y - min_y)
                scaled_line.append((scaled_x, scaled_y))
            scaled_lines_special.append(scaled_line)

        color = self.poster.colors["track"]
        color_special = self.poster.colors["special"]

        for line in scaled_lines:
            d.add(d.polyline(points=line, stroke=color, stroke_opacity=0.1, fill='none', stroke_width=5.0, stroke_linejoin='round', stroke_linecap='round'))
        for line in scaled_lines:
            d.add(d.polyline(points=line, stroke=color, stroke_opacity=0.2, fill='none', stroke_width=2.0, stroke_linejoin='round', stroke_linecap='round'))
        for line in scaled_lines:
            d.add(d.polyline(points=line, stroke=color, fill='none', stroke_width=0.3, stroke_linejoin='round', stroke_linecap='round'))
        for line in scaled_lines_special:
            d.add(d.polyline(points=line, stroke=color_special, fill='none', stroke_width=0.3, stroke_linejoin='round', stroke_linecap='round'))
