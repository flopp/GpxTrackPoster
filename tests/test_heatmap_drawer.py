"""
Several tests for HeatmapDrawer
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import math
from argparse import ArgumentParser
from typing import List, Optional

import pytest
import s2sphere  # type: ignore

from gpxtrackposter.cli import create_parser, parse_args
from gpxtrackposter.exceptions import ParameterError
from gpxtrackposter.heatmap_drawer import HeatmapDrawer
from gpxtrackposter.poster import Poster


@pytest.fixture(name="heatmap_drawer")
def fixture_heatmap_drawer() -> HeatmapDrawer:
    """Return a HeatmapDrawer"""
    return HeatmapDrawer(Poster())


@pytest.fixture(name="parser")
def fixture_parser() -> ArgumentParser:
    """Return an ArgParser"""
    return create_parser()


@pytest.mark.parametrize(
    "invalid_center",
    ["-10,0,10", "-10;10", "-10.10"],
)
def test_validate_heatmap_center_with_invalid_center_string_raises_exception(
    invalid_center: str, heatmap_drawer: HeatmapDrawer
) -> None:
    with pytest.raises(ParameterError):
        heatmap_drawer.validate_heatmap_center(invalid_center)


@pytest.mark.parametrize(
    "invalid_center",
    ["A,B", "A,10", "-10,B"],
)
def test_validate_heatmap_center_with_invalid_center_type_raises_exception(
    invalid_center: str, heatmap_drawer: HeatmapDrawer
) -> None:
    with pytest.raises(ParameterError):
        heatmap_drawer.validate_heatmap_center(invalid_center)


@pytest.mark.parametrize(
    "invalid_center",
    ["-91, 10", "-90, -181", "91, 10", "-91, 181", "-91, -181"],
)
def test_validate_heatmap_center_with_invalid_center_values_raises_exception(
    invalid_center: str, heatmap_drawer: HeatmapDrawer
) -> None:
    with pytest.raises(ParameterError):
        heatmap_drawer.validate_heatmap_center(invalid_center)


@pytest.mark.parametrize(
    "valid_center, expected_result",
    [
        ("-10, 10", s2sphere.LatLng.from_degrees(-10, 10)),
        ("-10,10", s2sphere.LatLng.from_degrees(-10, 10)),
        (" -10, 10 ", s2sphere.LatLng.from_degrees(-10, 10)),
        ("-90, -180", s2sphere.LatLng.from_degrees(-90, -180)),
        ("90, 180", s2sphere.LatLng.from_degrees(90, 180)),
        ("0, 0", s2sphere.LatLng.from_degrees(0, 0)),
    ],
)
def test_validate_heatmap_center_with_valid_center_returns_center(
    valid_center: str, expected_result: s2sphere.LatLng, heatmap_drawer: HeatmapDrawer
) -> None:
    assert expected_result == heatmap_drawer.validate_heatmap_center(valid_center)


def test_validate_heatmap_radius_with_invalid_value_raises_exception(heatmap_drawer: HeatmapDrawer) -> None:
    with pytest.raises(ParameterError):
        heatmap_drawer.validate_heatmap_radius(-10.0)


def test_validate_heatmap_radius_without_center_raises_exception(heatmap_drawer: HeatmapDrawer) -> None:
    with pytest.raises(ParameterError):
        assert heatmap_drawer._center is None  # pylint: disable=protected-access
        heatmap_drawer.validate_heatmap_radius(10.0)


@pytest.mark.parametrize(
    "valid_radius, expected_result",
    [(0.1, 0.1), (10.0, 10.0)],
)
def test_validate_heatmap_radius_with_valid_radius_returns_radius(
    valid_radius: float, expected_result: float, heatmap_drawer: HeatmapDrawer
) -> None:
    heatmap_drawer.validate_heatmap_center("-10,10")
    assert expected_result == heatmap_drawer.validate_heatmap_radius(valid_radius)


@pytest.mark.parametrize(
    "invalid_string",
    [
        "0.1,5.0, 0.2,2.0",
        "0.1,5.0, 0.2,2.0, 1.0,0.3, 0.1, 0.3",
    ],
)
def test_validate_heatmap_line_width_with_invalid_string_raises_exception(
    invalid_string: str, heatmap_drawer: HeatmapDrawer
) -> None:
    with pytest.raises(ParameterError):
        heatmap_drawer.validate_heatmap_line_width(invalid_string)


@pytest.mark.parametrize(
    "invalid_string",
    [
        "1.1,5.0, 0.2,2.0, 1.0,0.3",
        "0.1,5.0, 1.1,2.0, 1.0,0.3",
        "0.1,5.0, 0.2,2.0, 1.1,0.3",
    ],
)
def test_validate_heatmap_line_width_with_invalid_value_raises_exception(
    invalid_string: str, heatmap_drawer: HeatmapDrawer
) -> None:
    with pytest.raises(ParameterError):
        heatmap_drawer.validate_heatmap_line_width(invalid_string)


@pytest.mark.parametrize(
    "valid_string, expected_result",
    [
        ("automatic", None),
        ("AUTOMATIC", None),
        ("0.1,5.0, 0.2,2.0, 1.0,0.3", [(0.1, 5.0), (0.2, 2.0), (1.0, 0.3)]),
    ],
)
def test_validate_heatmap_line_width_with_valid_value_returns_line_widths(
    valid_string: str, expected_result: Optional[List], heatmap_drawer: HeatmapDrawer
) -> None:
    assert expected_result == heatmap_drawer.validate_heatmap_line_width(valid_string)


def test_validate_heatmap_line_width_without_value_returns_none(heatmap_drawer: HeatmapDrawer) -> None:
    assert heatmap_drawer.validate_heatmap_line_width() is None


@pytest.mark.parametrize(
    "valid_string, expected_result",
    [
        ("0.1,5.0, 0.2,2.0, 1.0,0.3", [(0.1, 5.0), (0.2, 2.0), (1.0, 0.3)]),
        ("0.1,5.0,0.2,2.0,1.0,0.3", [(0.1, 5.0), (0.2, 2.0), (1.0, 0.3)]),
        (" 0.1,5.0, 0.2,2.0, 1.0,0.3 ", [(0.1, 5.0), (0.2, 2.0), (1.0, 0.3)]),
    ],
)
def test_get_line_transparencies_and_widths_with_values_returns_values(
    valid_string: str, expected_result: Optional[List], heatmap_drawer: HeatmapDrawer
) -> None:
    assert expected_result == heatmap_drawer.validate_heatmap_line_width(valid_string)


@pytest.mark.parametrize(
    "name, test_value1, test_value2, expected_result",
    [
        (
            "freiburg_newyork_6244.7km_larger_max_distance",
            (47.99472, 7.84972),
            (40.7306, -73.9866),
            [(0.02, 0.5), (0.05, 0.2), (1.0, 0.05)],
        ),
        (
            "berlin_paris_884km",
            (52.51944, 13.40667),
            (48.725823, 2.372662),
            [(0.028383, 0.971593), (0.065719, 0.388637), (1.000000, 0.076199)],
        ),
        (
            "amsterdam_paris_431.4km",
            (52.378000, 4.900000),
            (48.859489, 2.320582),
            [(0.065106, 3.037229), (0.134574, 1.214891), (1.000000, 0.190957)],
        ),
        (
            "amsterdam_brussels_174.4km",
            (52.378, 4.90000),
            (50.8467, 4.3547),
            [(0.085898, 4.206781), (0.173559, 1.682712), (1.000000, 0.255932)],
        ),
        (
            "amsterdam_rotterdam_57.9km",
            (52.378, 4.90000),
            (51.950, 4.41667),
            [(0.095314, 4.736450), (0.191215, 1.894580), (1.000000, 0.285358)],
        ),
        (
            "dortmund_gelsenkirchen_25.3km",
            (51.51389, 7.46528),
            (51.51667, 7.10000),
            [(0.097950, 4.884733), (0.196157, 1.953893), (1.000000, 0.293596)],
        ),
        (
            "hoofddorp_shiphol_6.6km_smaller_min_distance",
            (52.3, 4.66667),
            (52.30857425000001, 4.76293775),
            [(0.1, 5.0), (0.2, 2.0), (1.0, 0.3)],
        ),
    ],
)
def test_get_line_transparencies_and_widths_with_automatic_returns_calculated_values(
    name: str, test_value1: tuple, test_value2: tuple, expected_result: list, heatmap_drawer: HeatmapDrawer
) -> None:
    bbox = s2sphere.sphere.LatLngRect.from_point_pair(
        s2sphere.LatLng.from_degrees(test_value1[0], test_value1[1]),
        s2sphere.LatLng.from_degrees(test_value2[0], test_value2[1]),
    )
    print(name)
    result = heatmap_drawer.get_line_transparencies_and_widths(bbox)
    for pair in [0, 2]:
        for value in [0, 1]:
            math.isclose(expected_result[pair][value], result[pair][value], rel_tol=0.0001)


def test_parser_with_type_heatmap_sets_type(heatmap_drawer: HeatmapDrawer, parser: ArgumentParser) -> None:
    heatmap_drawer.create_args(parser)
    parsed = parse_args(parser, ["--type", "heatmap"])
    assert parsed.type
    assert parsed.type == "heatmap"


def test_parser_without_center_sets_none(heatmap_drawer: HeatmapDrawer, parser: ArgumentParser) -> None:
    heatmap_drawer.create_args(parser)
    parsed = parser.parse_args(["--type", "heatmap"])
    assert parsed.heatmap_center is None


def test_parser_with_center_sets_float_value(heatmap_drawer: HeatmapDrawer, parser: ArgumentParser) -> None:
    heatmap_drawer.create_args(parser)
    lat_lng = "47.99472, 7.84972"
    parsed = parser.parse_args(["--type", "heatmap", "--heatmap-center", lat_lng])
    assert parsed.heatmap_center
    assert parsed.heatmap_center == lat_lng


def test_parser_without_radius_sets_none(heatmap_drawer: HeatmapDrawer, parser: ArgumentParser) -> None:
    heatmap_drawer.create_args(parser)
    parsed = parser.parse_args(["--type", "heatmap"])
    assert parsed.heatmap_radius is None


def test_parser_with_radius_sets_float_value(heatmap_drawer: HeatmapDrawer, parser: ArgumentParser) -> None:
    heatmap_drawer.create_args(parser)
    parsed = parser.parse_args(["--type", "heatmap", "--heatmap-radius", "10.0"])
    assert parsed.heatmap_radius
    assert parsed.heatmap_radius == 10.0


@pytest.mark.parametrize(
    "name, test_value1, test_value2",
    [
        ("freiburg_newyork_6244.7km_larger_max_distance", (47.99472, 7.84972), (40.7306, -73.9866)),
        ("hoofddorp_shiphol_6.6km_smaller_min_distance", (52.3, 4.66667), (52.30857425000001, 4.76293775)),
    ],
)
def test_get_line_transparencies_and_widths_with_predefined_values_returns_predefined_values(
    name: str,
    test_value1: tuple,
    test_value2: tuple,
    heatmap_drawer: HeatmapDrawer,
    parser: ArgumentParser,
) -> None:
    heatmap_drawer.create_args(parser)
    line_width = "0.2,4.0, 0.3,3.0, 1.0,1.0"
    expected_line_width = [(0.2, 4.0), (0.3, 3.0), (1.0, 1.0)]
    parsed = parser.parse_args(
        [
            "--type",
            "heatmap",
            "--heatmap-center",
            "47.99472, 7.84972",
            "--heatmap-radius",
            "10.0",
            "--heatmap-line-transparency-width",
            line_width,
        ]
    )
    print(name)
    heatmap_drawer.fetch_args(parsed)
    assert parsed.heatmap_center
    assert parsed.heatmap_radius
    bbox = s2sphere.sphere.LatLngRect.from_point_pair(
        s2sphere.LatLng.from_degrees(test_value1[0], test_value1[1]),
        s2sphere.LatLng.from_degrees(test_value2[0], test_value2[1]),
    )
    assert parsed.heatmap_line_width
    assert line_width == parsed.heatmap_line_width
    assert expected_line_width == heatmap_drawer.get_line_transparencies_and_widths(bbox)
    assert expected_line_width == heatmap_drawer._heatmap_line_width  # pylint: disable=protected-access
