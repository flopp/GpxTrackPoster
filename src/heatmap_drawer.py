# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from . import tracks_drawer
from . import utils


class HeatmapDrawer(tracks_drawer.TracksDrawer):
    def __init__(self):
        super().__init__()

    def draw(self, poster, d, w, h, offset_x, offset_y):
        self.poster = poster

        xy_polylines = []
        xy_polylines_special = []
        for track in self.poster._tracks:
            track_xy = []
            for polyline in track.polylines:
                track_xy.append([utils.latlng2xy(lat, lng) for (lat, lng) in polyline])
            if not track.special:
                xy_polylines.extend(track_xy)
            else:
                xy_polylines_special.extend(track_xy)

        range_x, range_y = utils.compute_bounds_xy(xy_polylines)
        d_x = range_x.diameter()
        d_y = range_y.diameter()

        # compute scale
        scale = w/d_x if w/h <= d_x/d_y else h/d_y

        # compute offsets such that projected track is centered in its rect
        offset_x += 0.5 * w - 0.5 * scale * d_x
        offset_y += 0.5 * h - 0.5 * scale * d_y

        for lines, color in [(xy_polylines, self.poster.colors["track"]),
                             (xy_polylines_special, self.poster.colors["special"])]:
            scaled_lines = []
            for line in xy_polylines:
                scaled_line = []
                for (x, y) in line:
                    scaled_x = offset_x + scale * (x - range_x.lower())
                    scaled_y = offset_y + scale * (y - range_y.lower())
                    scaled_line.append((scaled_x, scaled_y))
                scaled_lines.append(scaled_line)
            for opacity, width in [(0.1, 5.0), (0.2, 2.0), (1.0, 0.3)]:
                for line in scaled_lines:
                    d.add(d.polyline(points=line, stroke=color, stroke_opacity=opacity,
                                     stroke_width=width, stroke_linejoin='round', stroke_linecap='round'))
