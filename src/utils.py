# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import colour
import math
import typing
from . import value_range


# mercator projection
def latlng2xy(lat: float, lng: float) -> (float, float):
    return lng/180+1, 0.5-math.log(math.tan(math.pi/4*(1+lat/90)))/math.pi


def compute_bounds_xy(polylines: typing.List[float, float]) -> (value_range.ValueRange, value_range.ValueRange):
    range_x = value_range.ValueRange()
    range_y = value_range.ValueRange()
    for line in polylines:
        for (x, y) in line:
            range_x.extend(x)
            range_y.extend(y)
    return range_x, range_y


def compute_grid(count: int, width: float, height: float) -> (float, (int, int)):
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


def interpolate_color(color1: str, color2: str, ratio: float) -> str:
    c1 = colour.Color(color1)
    c2 = colour.Color(color2)
    c3 = colour.Color(hue=((1 - ratio) * c1.hue + ratio * c2.hue),
                      saturation=((1 - ratio) * c1.saturation + ratio * c2.saturation),
                      luminance=((1 - ratio) * c1.luminance + ratio * c2.luminance))
    return c3.hex_l
