# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import svgwrite
import s2sphere as s2
from .poster import Poster
from .tracks_drawer import TracksDrawer
from .xy import XY
from . import utils


class HeatmapDrawer(TracksDrawer):
    def __init__(self, the_poster: Poster):
        super().__init__(the_poster)

    def draw(self, dr: svgwrite.Drawing, size: XY, offset: XY):
        bbox = s2.LatLngRect()
        for tr in self.poster.tracks:
            bbox = bbox.union(tr.bbox())

        normal_lines = []
        special_lines = []
        for tr in self.poster.tracks:
            for line in utils.project(bbox, size, offset, tr.polylines):
                if tr.special:
                    special_lines.append(line)
                else:
                    normal_lines.append(line)
        for lines, color in [(normal_lines, self.poster.colors['track']),
                             (special_lines, self.poster.colors['special'])]:
            for opacity, width in [(0.1, 5.0), (0.2, 2.0), (1.0, 0.3)]:
                for line in lines:
                    dr.add(dr.polyline(points=line, stroke=color, stroke_opacity=opacity, fill='none',
                                       stroke_width=width, stroke_linejoin='round', stroke_linecap='round'))
