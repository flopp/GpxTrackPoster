# Copyright 2018 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from gpxtrackposter.utils import interpolate_color


def test_interpolate_color():
    assert interpolate_color('#000000', '#ffffff', 0) == '#000000'
    assert interpolate_color('#000000', '#ffffff', 1) == '#ffffff'
    assert interpolate_color('#000000', '#ffffff', 0.5) == '#7f7f7f'
    assert interpolate_color('#000000', '#ffffff', -100) == '#000000'
    assert interpolate_color('#000000', '#ffffff', 12345) == '#ffffff'
