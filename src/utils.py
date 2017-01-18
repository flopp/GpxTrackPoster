# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import math


# mercator projection
def latlng2xy(lat, lng):
    return lng/180+1, 0.5-math.log(math.tan(math.pi/4*(1+lat/90)))/math.pi


def compute_bounds_xy(polylines):
    min_x = None
    max_x = None
    min_y = None
    max_y = None
    for line in polylines:
        for (x, y) in line:
            if min_x is None:
                min_x = x
                max_x = x
                min_y = y
                max_y = y
            else:
                min_x = min(x, min_x)
                max_x = max(x, max_x)
                min_y = min(y, min_y)
                max_y = max(y, max_y)
    return min_x, min_y, max_x, max_y
