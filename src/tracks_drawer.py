# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from . import utils


class TracksDrawer:
    def __init__(self):
        self.poster = None

    def draw(self, poster, d, w, h, offset_x, offset_y):
        pass

    def color(self, length_range, length, is_special=False):
        assert length_range.is_valid()
        assert length_range.contains(length)

        color1 = self.poster.colors['special'] if is_special else self.poster.colors['track']
        color2 = self.poster.colors['special2'] if is_special else self.poster.colors['track2']

        diff = length_range.diameter()
        if diff == 0:
            return color1

        return utils.interpolate_color(color1, color2, (length - length_range.lower()) / diff)
