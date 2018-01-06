# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import argparse
import calendar
import datetime
import math
import svgwrite
from typing import List, Optional
from .poster import Poster
from .track import Track
from .tracks_drawer import TracksDrawer
from .value_range import ValueRange
from .xy import XY
from . import utils


class CircularDrawer(TracksDrawer):
    def __init__(self, the_poster: Poster):
        super().__init__(the_poster)
        self._rings = False
        self._ring_color = 'darkgrey'

    def create_args(self, args_parser: argparse.ArgumentParser):
        group = args_parser.add_argument_group('Circular Type Options')
        group.add_argument('--circular-rings', dest='circular_rings', action='store_true', help='Draw distance rings.')
        group.add_argument('--circular-ring-color', dest='circular_ring_color', metavar='COLOR', type=str,
                           default='darkgrey', help='Color of distance rings.')

    def fetch_args(self, args):
        self._rings = args.circular_rings
        self._ring_color = args.circular_ring_color

    def draw(self, d: svgwrite.Drawing, size: XY, offset: XY):
        if self.poster.length_range_by_date is None:
            return

        years = self.poster.years.count()
        _, (count_x, count_y) = utils.compute_grid(years, size)
        x, y = 0, 0
        cell_size = size * XY(1 / count_x, 1 / count_y)
        margin = XY(4, 4)
        if count_x <= 1:
            margin.x = 0
        if count_y <= 1:
            margin.y = 0
        sub_size = cell_size - 2 * margin
        for year in range(self.poster.years.from_year, self.poster.years.to_year + 1):
            self._draw_year(d, sub_size, offset + margin + cell_size * XY(x, y), year)
            x += 1
            if x >= count_x:
                x = 0
                y += 1

    def _draw_year(self, d: svgwrite.Drawing, size: XY, offset: XY, year: int):
        min_size = min(size.x, size.y)
        outer_radius = 0.5 * min_size - 6
        radius_range = ValueRange.from_pair(outer_radius / 4, outer_radius)
        center = offset + 0.5 * size

        if self._rings:
            self._draw_rings(d, center, radius_range)

        year_style = 'dominant-baseline: central; font-size:{}px; font-family:Arial;'.format(min_size * 4.0 / 80.0)
        month_style = 'font-size:{}px; font-family:Arial;'.format(min_size * 3.0 / 80.0)

        d.add(d.text('{}'.format(year), insert=center.tuple(), fill=self.poster.colors['text'], text_anchor="middle",
                     alignment_baseline="middle", style=year_style))
        df = 360.0 / (366 if calendar.isleap(year) else 365)
        day = 0
        date = datetime.date(year, 1, 1)
        while date.year == year:
            text_date = date.strftime("%Y-%m-%d")
            a1 = math.radians(day * df)
            a2 = math.radians((day + 1) * df)
            if date.day == 1:
                (_, last_day) = calendar.monthrange(date.year, date.month)
                a3 = math.radians((day + last_day - 1) * df)
                sin_a1, cos_a1 = math.sin(a1), math.cos(a1)
                sin_a3, cos_a3 = math.sin(a3), math.cos(a3)
                r1 = outer_radius + 1
                r2 = outer_radius + 6
                r3 = outer_radius + 2
                d.add(d.line(
                    start=(center + r1 * XY(sin_a1, -cos_a1)).tuple(),
                    end=(center + r2 * XY(sin_a1, -cos_a1)).tuple(),
                    stroke=self.poster.colors['text'],
                    stroke_width=0.3))
                path = d.path(d=('M', center.x + r3 * sin_a1, center.y - r3 * cos_a1), fill='none', stroke='none')
                path.push('a{},{} 0 0,1 {},{}'.format(r3, r3, r3 * (sin_a3 - sin_a1), r3 * (cos_a1 - cos_a3)))
                d.add(path)
                tpath = svgwrite.text.TextPath(path, date.strftime("%B"), startOffset=(0.5 * r3 * (a3 - a1)))
                text = d.text("", fill=self.poster.colors['text'], text_anchor="middle", style=month_style)
                text.add(tpath)
                d.add(text)
            if text_date in self.poster.tracks_by_date:
                self._draw_circle_segment(d, self.poster.tracks_by_date[text_date], a1, a2, radius_range, center)

            day += 1
            date += datetime.timedelta(1)

    def _determine_ring_distance(self) -> Optional[float]:
        length_range = self.poster.length_range_by_date
        ring_distance = None
        for distance in [1, 5, 10, 50]:
            if self.poster.units != 'metric':
                # convert from miles to meters
                distance *= 1609.344
            else:
                # convert from km to meters
                distance *= 1000
            if length_range.upper() < distance:
                continue
            ring_distance = distance
            if (length_range.upper() / distance) <= 5:
                break
        return ring_distance

    def _draw_rings(self, d: svgwrite.Drawing, center: XY, radius_range: ValueRange):
        length_range = self.poster.length_range_by_date
        ring_distance = self._determine_ring_distance()
        if ring_distance is None:
            return
        distance = ring_distance
        while distance < length_range.upper():
            radius = radius_range.lower() + radius_range.diameter() * distance / length_range.upper()
            d.add(d.circle(center=center.tuple(), r=radius, stroke=self._ring_color, stroke_opacity='0.2',
                           fill='none', stroke_width=0.3))
            distance += ring_distance

    def _draw_circle_segment(self, d: svgwrite.Drawing, tracks: List[Track], a1: float, a2: float,
                             rr: ValueRange, center: XY):
        length = sum([t.length for t in tracks])
        color = self.color(self.poster.length_range_by_date, length, [t for t in tracks if t.special])
        r1 = rr.lower()
        r2 = rr.lower() + rr.diameter() * length / self.poster.length_range_by_date.upper()
        sin_a1, cos_a1 = math.sin(a1), math.cos(a1)
        sin_a2, cos_a2 = math.sin(a2), math.cos(a2)
        path = d.path(d=('M', center.x + r1 * sin_a1, center.y - r1 * cos_a1), fill=color, stroke='none')
        path.push('l', (r2 - r1) * sin_a1, (r1 - r2) * cos_a1)
        path.push('a{},{} 0 0,0 {},{}'.format(r2, r2, r2 * (sin_a2 - sin_a1), r2 * (cos_a1 - cos_a2)))
        path.push('l', (r1 - r2) * sin_a2, (r2 - r1) * cos_a2)
        d.add(path)
