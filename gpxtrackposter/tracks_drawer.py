"""Contains the base class TracksDrawer, which other Drawers inherit from."""
# Copyright 2016-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import argparse

import pint  # type: ignore
import svgwrite  # type: ignore

from gpxtrackposter import utils
from gpxtrackposter.poster import Poster
from gpxtrackposter.quantity_range import QuantityRange
from gpxtrackposter.xy import XY


class TracksDrawer:
    """Base class that other drawer classes inherit from."""

    def __init__(self, the_poster: Poster):
        self.poster = the_poster

    def create_args(self, args_parser: argparse.ArgumentParser) -> None:
        pass

    def fetch_args(self, args: argparse.Namespace) -> None:
        pass

    def draw(self, dr: svgwrite.Drawing, g: svgwrite.container.Group, size: XY, offset: XY) -> None:
        pass

    def color(self, length_range: QuantityRange, length: pint.quantity.Quantity, is_special: bool = False) -> str:
        color1 = self.poster.colors["special"] if is_special else self.poster.colors["track"]
        color2 = self.poster.colors["special2"] if is_special else self.poster.colors["track2"]
        return utils.interpolate_color(color1, color2, length_range.relative_position(length))
