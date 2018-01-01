# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import svgwrite
from . import poster
from . import track
from . import tracks_drawer
from . import utils


class GridDrawer(tracks_drawer.TracksDrawer):
    def __init__(self, the_poster: poster.Poster):
        super().__init__(the_poster)

    def draw(self, d: svgwrite.Drawing, w: float, h: float, offset_x: float, offset_y: float):
        size, (count_x, count_y) = utils.compute_grid(len(self.poster.tracks), w, h)
        spacing_x = 0 if count_x <= 1 else (w - size * count_x) / (count_x - 1)
        spacing_y = 0 if count_y <= 1 else (h - size * count_y) / (count_y - 1)
        offset_x += (w - count_x * size - (count_x - 1) * spacing_x) / 2
        offset_y += (h - count_y * size - (count_y - 1) * spacing_y) / 2
        for (index, tr) in enumerate(self.poster.tracks):
            x = index % count_x
            y = index // count_x
            self.__draw_track(d, tr, offset_x + (0.05 + x) * size + x * spacing_x,
                              offset_y + (0.05 + y) * size + y * spacing_y,
                              0.9 * size, 0.9 * size)

    def __draw_track(self, d: svgwrite.Drawing, tr: track.Track, x_offset: float, y_offset: float, width: float,
                     height: float):
        # compute mercator projection of track segments
        lines = []
        for polyline in tr.polylines:
            lines.append([utils.latlng2xy(latlng) for latlng in polyline])

        # compute bounds
        range_x, range_y = utils.compute_bounds_xy(lines)
        d_x = range_x.diameter()
        d_y = range_y.diameter()

        # compute scale
        scale = width / d_x
        if width / height > d_x / d_y:
            scale = height / d_y

        # compute offsets such that projected track is centered in its rect
        x_offset += 0.5 * width - 0.5 * scale * d_x
        y_offset += 0.5 * height - 0.5 * scale * d_y

        color = self.color(self.poster.length_range, tr.length, tr.special)

        for line in lines:
            scaled_line = []
            for (x, y) in line:
                scaled_x = x_offset + scale * (x - range_x.lower())
                scaled_y = y_offset + scale * (y - range_y.lower())
                scaled_line.append((scaled_x, scaled_y))
            d.add(d.polyline(points=scaled_line, stroke=color, fill='none',
                             stroke_width=0.5, stroke_linejoin='round', stroke_linecap='round'))
