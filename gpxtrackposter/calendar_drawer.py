"""Draw a calendar poster."""
# Copyright 2016-2022 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import calendar
import datetime

import pint  # type: ignore
import svgwrite  # type: ignore

from gpxtrackposter import utils
from gpxtrackposter.exceptions import PosterError
from gpxtrackposter.localization import localized_day_of_week_name
from gpxtrackposter.poster import Poster
from gpxtrackposter.tracks_drawer import TracksDrawer
from gpxtrackposter.xy import XY


class CalendarDrawer(TracksDrawer):
    """Draw a calendar poster."""

    def __init__(self, the_poster: Poster):
        super().__init__(the_poster)

    def draw(self, dr: svgwrite.Drawing, g: svgwrite.container.Group, size: XY, offset: XY) -> None:
        """Iterate through the Poster's years, creating a calendar for each."""
        if len(self.poster.tracks) == 0:
            raise PosterError("No tracks to draw.")
        years = self.poster.years.count()
        _, counts = utils.compute_grid(years, size)
        if counts is None:
            raise PosterError("Unable to compute grid.")
        count_x, count_y = counts[0], counts[1]
        x, y = 0, 0
        cell_size = size * XY(1 / count_x, 1 / count_y)
        margin = XY(4, 8)
        if count_x <= 1:
            margin.x = 0
        if count_y <= 1:
            margin.y = 0
        sub_size = cell_size - 2 * margin

        for year in self.poster.years.iter():
            g_year = dr.g(id=f"year{year}")
            g.add(g_year)
            self._draw(dr, g_year, sub_size, offset + margin + cell_size * XY(x, y), year)
            x += 1
            if x >= count_x:
                x = 0
                y += 1

    def _draw(self, dr: svgwrite.Drawing, g: svgwrite.container.Group, size: XY, offset: XY, year: int) -> None:
        min_size = min(size.x, size.y)
        year_size = min_size * 4.0 / 80.0
        year_style = f"font-size:{year_size}px; font-family:Arial;"
        month_style = f"font-size:{min_size * 3.0 / 80.0}px; font-family:Arial;"
        day_style = f"dominant-baseline: central; font-size:{min_size * 1.0 / 80.0}px; font-family:Arial;"
        day_length_style = f"font-size:{min_size * 1.0 / 80.0}px; font-family:Arial;"

        g.add(
            dr.text(
                f"{year}",
                insert=offset.tuple(),
                fill=self.poster.colors["text"],
                alignment_baseline="hanging",
                style=year_style,
            )
        )
        offset.y += year_size
        size.y -= year_size
        count_x = 31
        for month in range(1, 13):
            date = datetime.date(year, month, 1)
            (_, last_day) = calendar.monthrange(year, month)
            count_x = max(count_x, date.weekday() + last_day)

        cell_size = min(size.x / count_x, size.y / 36)
        spacing = XY(
            (size.x - cell_size * count_x) / (count_x - 1),
            (size.y - cell_size * 3 * 12) / 11,
        )

        for month in range(1, 13):
            date = datetime.date(year, month, 1)
            y = month - 1
            y_pos = offset.y + (y * 3 + 1) * cell_size + y * spacing.y
            g.add(
                dr.text(
                    self.poster.month_name(month),
                    insert=(offset.x, y_pos - 2),
                    fill=self.poster.colors["text"],
                    alignment_baseline="hanging",
                    style=month_style,
                )
            )

            day_offset = date.weekday()
            while date.month == month:
                x = date.day - 1
                x_pos = offset.x + (day_offset + x) * cell_size + x * spacing.x
                pos = (x_pos + 0.05 * cell_size, y_pos + 1.15 * cell_size)
                dim = (cell_size * 0.9, cell_size * 0.9)
                text_date = date.strftime("%Y-%m-%d")
                if text_date in self.poster.tracks_by_date:
                    tracks = self.poster.tracks_by_date[text_date]
                    length = pint.quantity.Quantity(sum([t.length() for t in tracks]))
                    has_special = len([t for t in tracks if t.special]) > 0
                    color = self.color(self.poster.length_range_by_date, length, has_special)
                    g.add(dr.rect(pos, dim, fill=color))
                    g.add(
                        dr.text(
                            utils.format_float(self.poster.m2u(length)),
                            insert=(
                                pos[0] + cell_size / 2,
                                pos[1] + cell_size + cell_size / 2,
                            ),
                            text_anchor="middle",
                            style=day_length_style,
                            fill=self.poster.colors["text"],
                        )
                    )
                else:
                    g.add(dr.rect(pos, dim, fill="#444444"))

                g.add(
                    dr.text(
                        localized_day_of_week_name(date.weekday(), short=True),
                        insert=(
                            offset.x + (day_offset + x) * cell_size + cell_size / 2,
                            pos[1] + cell_size / 2,
                        ),
                        text_anchor="middle",
                        alignment_baseline="middle",
                        style=day_style,
                    )
                )
                date += datetime.timedelta(1)
