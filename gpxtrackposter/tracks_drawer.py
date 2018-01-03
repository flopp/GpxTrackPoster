# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import argparse
import svgwrite
from . import poster
from . import utils
from . import value_range


class TracksDrawer:
    def __init__(self, the_poster: poster.Poster):
        self.poster = the_poster

    def create_args(self, args_parser: argparse.ArgumentParser):
        pass

    def fetch_args(self, args):
        pass

    def draw(self, d: svgwrite.Drawing, w: float, h: float, offset_x: float, offset_y: float):
        pass

    def color(self, length_range: value_range.ValueRange, length: float, is_special: bool=False) -> str:
        assert length_range.is_valid()
        assert length_range.contains(length)

        color1 = self.poster.colors['special'] if is_special else self.poster.colors['track']
        color2 = self.poster.colors['special2'] if is_special else self.poster.colors['track2']

        diff = length_range.diameter()
        if diff == 0:
            return color1

        return utils.interpolate_color(color1, color2, (length - length_range.lower()) / diff)
