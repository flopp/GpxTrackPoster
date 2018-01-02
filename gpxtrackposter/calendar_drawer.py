# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import calendar
import datetime
import svgwrite
from . import poster
from . import tracks_drawer
from . import utils


class CalendarDrawer(tracks_drawer.TracksDrawer):
    def __init__(self, the_poster: poster.Poster):
        super().__init__(the_poster)

    def draw(self, d: svgwrite.Drawing, w: float, h: float, offset_x: float, offset_y: float):
        years = self.poster.years.count()
        _, (count_x, count_y) = utils.compute_grid(years, w, h)
        x, y = 0, 0
        ww, hh = w / count_x, h / count_y
        margin_x, margin_y = 4, 8
        if count_x <= 1:
            margin_x = 0
        if count_y <= 1:
            margin_y = 0
        www = ww - 2 * margin_x
        hhh = hh - 2 * margin_y

        for year in range(self.poster.years.from_year, self.poster.years.to_year + 1):
            self.__draw(d, www, hhh,
                        offset_x + ww * x + margin_x, offset_y + hh * y + margin_y,
                        year)
            x += 1
            if x >= count_x:
                x = 0
                y += 1

    def __draw(self, d, w: int, h: int, offset_x: int, offset_y: int, year):
        year_size = min(w, h) * 4.0 / 80.0
        year_style = 'font-size:{}px; font-family:Arial;'.format(year_size)
        month_style = 'font-size:{}px; font-family:Arial;'.format(min(w, h) * 3.0 / 80.0)
        day_style = 'font-size:{}px; font-family:Arial;'.format(min(w, h) * 1.0 / 80.0)
        day_length_style = 'font-size:{}px; font-family:Arial;'.format(min(w, h) * 1.0 / 80.0)

        d.add(d.text('{}'.format(year), insert=(offset_x, offset_y), fill=self.poster.colors['text'],
                     alignment_baseline="hanging", style=year_style))
        offset_y += year_size
        h = h - year_size
        count_x = 31
        for month in range(1, 13):
            date = datetime.date(year, month, 1)
            (_, last_day) = calendar.monthrange(year, month)
            count_x = max(count_x, date.weekday() + last_day)

        size = min(w / count_x, h / 36)
        spacing_x = (w - size * count_x) / (count_x - 1)
        spacing_y = (h - size * 3 * 12) / 11

        dow = ["M", "T", "W", "T", "F", "S", "S"]
        for month in range(1, 13):
            date = datetime.date(year, month, 1)
            y = month - 1
            y_pos = offset_y + (y * 3 + 1) * size + y * spacing_y
            d.add(d.text(date.strftime("%B"), insert=(offset_x, y_pos - 2), fill=self.poster.colors['text'],
                         alignment_baseline="hanging", style=month_style))

            day_offset = date.weekday()
            while date.month == month:
                x = date.day - 1
                x_pos = offset_x + (day_offset + x) * size + x * spacing_x
                pos = (x_pos + 0.05 * size, y_pos + 0.05 * size)
                dim = (size * 0.9, size * 0.9)
                text_date = date.strftime("%Y-%m-%d")
                if text_date in self.poster.tracks_by_date:
                    tracks = self.poster.tracks_by_date[text_date]
                    special = [t for t in tracks if t.special]
                    length = sum([t.length for t in tracks])
                    color = self.color(self.poster.length_range_by_date, length, special)
                    d.add(d.rect(pos, dim, fill=color))
                    d.add(d.text("{:.1f}".format(self.poster.m2u(length)),
                                 insert=(x_pos + size / 2, y_pos + size + size / 2),
                                 text_anchor="middle",
                                 style=day_length_style, fill=self.poster.colors['text']))
                else:
                    d.add(d.rect(pos, dim, fill='#444444'))

                d.add(d.text(dow[date.weekday()],
                             insert=(offset_x + (day_offset + x) * size + size / 2, y_pos + size / 2),
                             text_anchor="middle", alignment_baseline="middle",
                             style=day_style))
                date += datetime.timedelta(1)
