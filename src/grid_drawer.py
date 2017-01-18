# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from . import utils


class TracksDrawer:
    def __init__(self):
        self.poster = None

    def draw(self, poster, d, w, h, offset_x, offset_y):
        self.poster = poster
        size, (count_x, count_y) = self.__compute_grid(len(self.poster.tracks), w, h)
        spacing_x = 0 if count_x <= 1 else (w-size*count_x)/(count_x - 1)
        spacing_y = 0 if count_y <= 1 else (h-size*count_y)/(count_y - 1)
        offset_x += (w - count_x*size - (count_x - 1)*spacing_x)/2
        offset_y += (h - count_y*size - (count_y - 1)*spacing_y)/2
        for (index, track) in enumerate(self.poster.tracks):
            x = index % count_x
            y = index // count_x
            color = self.poster.colors['special'] if track.special else self.poster.colors['track']
            self.__draw_track(d, track, offset_x+(0.05 + x)*size+x*spacing_x, offset_y+(0.05+y)*size+y*spacing_y, 0.9 * size, 0.9 * size, color)

    def __compute_grid(self, count, width, height):
        # this is somehow suboptimal O(count^2). I guess it's possible in O(count)
        min_waste = -1
        best_counts = None
        best_size = None
        for count_x in range(1, count+1):
            size_x = width/count_x
            for count_y in range(1, count+1):
                if count_x * count_y >= count:
                    size_y = height/count_y
                    size = min(size_x, size_y)
                    waste = width*height - count*size*size
                    if waste < 0:
                        continue
                    elif best_size is None or waste < min_waste:
                        best_size = size
                        best_counts = count_x, count_y
                        min_waste = waste
        return best_size, best_counts

    def __draw_track(self, d, track, x_offset, y_offset, width, height, color):
        # compute mercator projection of track segments
        lines = []
        for polyline in track.polylines:
            lines.append([utils.latlng2xy(lat, lng) for (lat, lng) in polyline])

        # compute bounds
        (min_x, min_y, max_x, max_y) = utils.compute_bounds_xy(lines)
        d_x = max_x - min_x
        d_y = max_y - min_y

        # compute scale
        scale = width/d_x
        if width/height > d_x/d_y:
            scale = height/d_y

        # compute offsets such that projected track is centered in its rect
        x_offset += 0.5 * width - 0.5 * scale * d_x
        y_offset += 0.5 * height - 0.5 * scale * d_y

        scaled_lines = []
        for line in lines:
            scaled_line = []
            for (x, y) in line:
                scaled_x = x_offset + scale * (x - min_x)
                scaled_y = y_offset + scale * (y - min_y)
                scaled_line.append((scaled_x, scaled_y))
            scaled_lines.append(scaled_line)

        for line in scaled_lines:
            d.add(d.polyline(points=line, stroke=color, fill='none', stroke_width=0.5, stroke_linejoin='round', stroke_linecap='round'))
