# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import argparse
import logging
import svgwrite
import s2sphere as s2
from .exceptions import ParameterError
from .poster import Poster
from .tracks_drawer import TracksDrawer
from .xy import XY
from . import utils


log = logging.getLogger(__name__)


class HeatmapDrawer(TracksDrawer):
    def __init__(self, the_poster: Poster):
        super().__init__(the_poster)
        self._center = None

    def create_args(self, args_parser: argparse.ArgumentParser):
        group = args_parser.add_argument_group('Heatmap Type Options')
        group.add_argument('--heatmap-center', dest='heatmap_center', metavar='LAT,LNG', type=str,
                           help='Center of the heatmap (default: automatic).')

    def fetch_args(self, args: argparse.Namespace):
        self._center = None
        if args.heatmap_center:
            latlng_str = args.heatmap_center.split(',')
            if len(latlng_str) != 2:
                raise ParameterError('Not a valid LAT,LNG pair: {}'.format(args.heatmap_center))
            try:
                lat = float(latlng_str[0].strip())
                lng = float(latlng_str[1].strip())
            except ValueError as e:
                raise ParameterError('Not a valid LAT,LNG pair: {}'.format(args.heatmap_center)) from e
            if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                raise ParameterError('Not a valid LAT,LNG pair: {}'.format(args.heatmap_center))
            self._center = s2.LatLng.from_degrees(lat, lng)

    def _determine_bbox(self) -> s2.LatLngRect:
        if self._center:
            log.info('Forcing heatmap center to {}'.format(self._center))
            dlat, dlng = 0, 0
            for tr in self.poster.tracks:
                for line in tr.polylines:
                    for latlng in line:
                        d = abs(self._center.lat().degrees - latlng.lat().degrees)
                        dlat = max(dlat, d)
                        d = abs(self._center.lng().degrees - latlng.lng().degrees)
                        while d > 360:
                            d -= 360
                        if d > 180:
                            d = 360 - d
                        dlng = max(dlng, d)
            return s2.LatLngRect.from_center_size(self._center, s2.LatLng.from_degrees(2 * dlat, 2 * dlng))

        tracks_bbox = s2.LatLngRect()
        for tr in self.poster.tracks:
            tracks_bbox = tracks_bbox.union(tr.bbox())
        return tracks_bbox

    def draw(self, dr: svgwrite.Drawing, size: XY, offset: XY):
        normal_lines = []
        special_lines = []
        bbox = self._determine_bbox()
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
