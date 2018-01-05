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

        return
        xy_polylines = []
        xy_polylines_special = []
        for track in self.poster.tracks:
            track_xy = []
            for polyline in track.polylines:
                track_xy.append([utils.latlng2xy(latlng) for latlng in polyline])
            if not track.special:
                xy_polylines.extend(track_xy)
            else:
                xy_polylines_special.extend(track_xy)

        range_x, range_y = utils.compute_bounds_xy(xy_polylines)
        d = XY(range_x.diameter(), range_y.diameter())

        # compute scale
        scale = size.x/d.x if size.x/size.y <= d.x/d.y else size.y/d.y

        # compute offsets such that projected track is centered in its rect
        offset = offset + 0.5 * (size - scale * d) - scale * XY(range_x.lower(), range_y.lower())

        for lines, color in [(xy_polylines, self.poster.colors['track']),
                             (xy_polylines_special, self.poster.colors['special'])]:
            scaled_lines = []
            for line in lines:
                scaled_lines.append([(offset + scale * xy).tuple() for xy in line])
            for opacity, width in [(0.1, 5.0), (0.2, 2.0), (1.0, 0.3)]:
                for line in scaled_lines:
                    dr.add(dr.polyline(points=line, stroke=color, stroke_opacity=opacity, fill='none',
                                       stroke_width=width, stroke_linejoin='round', stroke_linecap='round'))
