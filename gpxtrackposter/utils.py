# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import colour
import math
from typing import List, Optional, Tuple
import s2sphere as s2
from .value_range import ValueRange
from .xy import XY


# mercator projection
def latlng2xy(latlng: s2.LatLng) -> XY:
    return XY(latlng.lng().degrees / 180 + 1,
              0.5 - math.log(math.tan(math.pi / 4 * (1 + latlng.lat().degrees / 90))) / math.pi)


def compute_bounds_xy(lines: List[List[XY]]) -> Tuple[ValueRange, ValueRange]:
    range_x = ValueRange()
    range_y = ValueRange()
    for line in lines:
        for xy in line:
            range_x.extend(xy.x)
            range_y.extend(xy.y)
    return range_x, range_y


def compute_grid(count: int, dimensions: XY) -> Tuple[Optional[float], Optional[Tuple[int, int]]]:
    # this is somehow suboptimal O(count^2). I guess it's possible in O(count)
    min_waste = -1
    best_counts = None
    best_size = None
    for count_x in range(1, count+1):
        size_x = dimensions.x / count_x
        for count_y in range(1, count+1):
            if count_x * count_y >= count:
                size_y = dimensions.y / count_y
                size = min(size_x, size_y)
                waste = dimensions.x * dimensions.y - count * size * size
                if waste < 0:
                    continue
                elif best_size is None or waste < min_waste:
                    best_size = size
                    best_counts = count_x, count_y
                    min_waste = waste
    return best_size, best_counts


def interpolate_color(color1: str, color2: str, ratio: float) -> str:
    if ratio < 0:
        ratio = 0
    elif ratio > 1:
        ratio = 1
    c1 = colour.Color(color1)
    c2 = colour.Color(color2)
    c3 = colour.Color(hue=((1 - ratio) * c1.hue + ratio * c2.hue),
                      saturation=((1 - ratio) * c1.saturation + ratio * c2.saturation),
                      luminance=((1 - ratio) * c1.luminance + ratio * c2.luminance))
    return c3.hex_l
