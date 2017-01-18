# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import calendar
import datetime


class TracksDrawer:
    def __init__(self):
        self.poster = None

    def draw(self, poster, d, w, h, offset_x, offset_y):
        self.poster = poster

        count_x = 31
        for month in range(1, 13):
            date = datetime.date(self.poster.year, month, 1)
            (_, last_day) = calendar.monthrange(self.poster.year, month)
            count_x = max(count_x, date.weekday() + last_day)

        size = min(w / count_x, h / 36)
        spacing_x = (w - size * count_x)/(count_x - 1)
        spacing_y = (h - size * 3 * 12)/11

        tracks_by_date = {}
        for track in self.poster.tracks:
            text_date = track.start_time.strftime("%Y-%m-%d")
            if text_date in tracks_by_date:
                tracks_by_date[text_date].append(track)
            else:
                tracks_by_date[text_date] = [track]

        dow = ["M", "T", "W", "T", "F", "S", "S"]
        for month in range(1, 13):
            date = datetime.date(self.poster.year, month, 1)
            y = month-1
            y_pos = offset_y + (y*3 + 1)*size + y*spacing_y
            d.add(d.text(date.strftime("%B"), insert=(offset_x, y_pos-2), fill=self.poster.colors['text'],
                         alignment_baseline="hanging", style="font-size:4px; font-family:Arial"))

            day_offset = date.weekday()
            while date.month == month:
                x = date.day-1
                x_pos = offset_x + (day_offset+x)*size + x*spacing_x
                pos = (x_pos + 0.05*size, y_pos + 0.05*size)
                dim = (size*0.9, size*0.9)
                text_date = date.strftime("%Y-%m-%d")
                if text_date in tracks_by_date:
                    tracks = tracks_by_date[text_date]
                    special = [t for t in tracks if t.special]
                    length = sum([t.length for t in tracks])/1000
                    if special:
                        d.add(d.rect(pos, dim, fill=self.poster.colors['special']))
                    else:
                        d.add(d.rect(pos, dim, fill=self.poster.colors['track']))
                    d.add(d.text("{:.1f}".format(length), insert=(x_pos + size/2, y_pos + size + size/2),
                                 text_anchor="middle",
                                 style="font-size:2px; font-family:Arial", fill=self.poster.colors['text']))
                else:
                    d.add(d.rect(pos, dim, fill='#444444'))

                d.add(d.text(dow[date.weekday()], insert=(offset_x + (day_offset + x)*size + size/2, y_pos + size/2),
                             text_anchor="middle", alignment_baseline="baseline", baseline_shift="-8%",
                             style="font-size:2px; font-family:Arial"))
                date += datetime.timedelta(1)
