"""Draw a grid poster."""
# Copyright 2016-2018 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import svgwrite
from .exceptions import PosterError
from .poster import Poster
from .track import Track
from .tracks_drawer import TracksDrawer
from .xy import XY
from . import utils


class GridDrawer(TracksDrawer):
    """Drawer used to draw a grid poster

    Methods:
        draw: For each track, draw it on the poster.
    """

    def __init__(self, the_poster: Poster):
        super().__init__(the_poster)

    def draw(self, dr: svgwrite.Drawing, size: XY, offset: XY):
        """For each track, draw it on the poster."""
        if self.poster.tracks is None:
            raise PosterError('No tracks to draw.')
        cell_size, counts = utils.compute_grid(len(self.poster.tracks), size)
        if cell_size is None or counts is None:
            raise PosterError('Unable to compute grid.')
        count_x, count_y = counts[0], counts[1]
        spacing_x = 0 if count_x <= 1 else (size.x - cell_size * count_x) / (count_x - 1)
        spacing_y = 0 if count_y <= 1 else (size.y - cell_size * count_y) / (count_y - 1)
        offset.x += (size.x - count_x * cell_size - (count_x - 1) * spacing_x) / 2
        offset.y += (size.y - count_y * cell_size - (count_y - 1) * spacing_y) / 2
        for (index, tr) in enumerate(self.poster.tracks):
            p = XY(index % count_x, index // count_x) * XY(cell_size + spacing_x, cell_size + spacing_y)
            self._draw_track(dr, tr,
                             0.9 * XY(cell_size, cell_size),
                             offset + 0.05 * XY(cell_size, cell_size) + p)

    def _draw_track(self, dr: svgwrite.Drawing, tr: Track, size: XY, offset: XY):
        color = self.color(self.poster.length_range, tr.length, tr.special)
        for line in utils.project(tr.bbox(), size, offset, tr.polylines):
            dr.add(dr.polyline(points=line, stroke=color, fill='none',
                               stroke_width=0.5, stroke_linejoin='round', stroke_linecap='round'))
