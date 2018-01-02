from gpxtrackposter.utils import interpolate_color


def test_interpolate_color():
    assert interpolate_color('#000000', '#ffffff', 0) == '#000000'
    assert interpolate_color('#000000', '#ffffff', 1) == '#ffffff'
    assert interpolate_color('#000000', '#ffffff', 0.5) == '#7f7f7f'
    assert interpolate_color('#000000', '#ffffff', -100) == '#000000'
    assert interpolate_color('#000000', '#ffffff', 12345) == '#ffffff'
