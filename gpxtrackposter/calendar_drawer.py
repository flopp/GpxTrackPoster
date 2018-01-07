# Copyright 2016-2018 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import calendar
import datetime
import svgwrite
from .poster import Poster
from .tracks_drawer import TracksDrawer
from .xy import XY
from . import utils


class CalendarDrawer(TracksDrawer):
    def __init__(self, the_poster: Poster):
        super().__init__(the_poster)

    def draw(self, d: svgwrite.Drawing, size: XY, offset: XY):
        years = self.poster.years.count()
        _, (count_x, count_y) = utils.compute_grid(years, size)
        x, y = 0, 0
        cell_size = size * XY(1 / count_x, 1 / count_y)
        margin = XY(4, 8)
        if count_x <= 1:
            margin.x = 0
        if count_y <= 1:
            margin.y = 0
        sub_size = cell_size - 2 * margin

        for year in range(self.poster.years.from_year, self.poster.years.to_year + 1):
            self._draw(d, sub_size, offset + margin + cell_size * XY(x, y), year)
            x += 1
            if x >= count_x:
                x = 0
                y += 1

    def _draw(self, d: svgwrite.Drawing, size: XY, offset: XY, year: int):
        min_size = min(size.x, size.y)
        year_size = min_size * 4.0 / 80.0
        year_style = 'font-size:{}px; font-family:Arial;'.format(year_size)
        month_style = 'font-size:{}px; font-family:Arial;'.format(min_size * 3.0 / 80.0)
        day_style = 'dominant-baseline: central; font-size:{}px; font-family:Arial;'.format(min_size * 1.0 / 80.0)
        day_length_style = 'font-size:{}px; font-family:Arial;'.format(min_size * 1.0 / 80.0)

        d.add(d.text('{}'.format(year), insert=offset.tuple(), fill=self.poster.colors['text'],
                     alignment_baseline="hanging", style=year_style))
        offset.y += year_size
        size.y -= year_size
        count_x = 31
        for month in range(1, 13):
            date = datetime.date(year, month, 1)
            (_, last_day) = calendar.monthrange(year, month)
            count_x = max(count_x, date.weekday() + last_day)

        cell_size = min(size.x / count_x, size.y / 36)
        spacing = XY((size.x - cell_size * count_x) / (count_x - 1), (size.y - cell_size * 3 * 12) / 11)

        dow = ["M", "T", "W", "T", "F", "S", "S"]
        for month in range(1, 13):
            date = datetime.date(year, month, 1)
            y = month - 1
            y_pos = offset.y + (y * 3 + 1) * cell_size + y * spacing.y
            d.add(d.text(date.strftime("%B"), insert=(offset.x, y_pos - 2), fill=self.poster.colors['text'],
                         alignment_baseline="hanging", style=month_style))

            day_offset = date.weekday()
            while date.month == month:
                x = date.day - 1
                x_pos = offset.x + (day_offset + x) * cell_size + x * spacing.x
                pos = (x_pos + 0.05 * cell_size, y_pos + 0.05 * cell_size)
                dim = (cell_size * 0.9, cell_size * 0.9)
                text_date = date.strftime("%Y-%m-%d")
                if text_date in self.poster.tracks_by_date:
                    tracks = self.poster.tracks_by_date[text_date]
                    length = sum([t.length for t in tracks])
                    color = self.color(self.poster.length_range_by_date, length, [t for t in tracks if t.special])
                    d.add(d.rect(pos, dim, fill=color))
                    d.add(d.text("{:.1f}".format(self.poster.m2u(length)),
                                 insert=(x_pos + cell_size / 2, y_pos + cell_size + cell_size / 2),
                                 text_anchor="middle",
                                 style=day_length_style, fill=self.poster.colors['text']))
                else:
                    d.add(d.rect(pos, dim, fill='#444444'))

                d.add(d.text(dow[date.weekday()],
                             insert=(offset.x + (day_offset + x) * cell_size + cell_size / 2, y_pos + cell_size / 2),
                             text_anchor="middle", alignment_baseline="middle",
                             style=day_style))
                date += datetime.timedelta(1)
