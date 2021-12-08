"""
Several tests for HeatmapDrawer
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import unittest

import s2sphere  # type: ignore

from gpxtrackposter.exceptions import ParameterError
from gpxtrackposter.heatmap_drawer import HeatmapDrawer
from gpxtrackposter.poster import Poster
from gpxtrackposter.cli import create_parser, parse_args


class TestCase(unittest.TestCase):
    """
    Test class for HeatmapDrawer
    """

    def setUp(self) -> None:
        self.poster = Poster()
        self.heatmap_drawer = HeatmapDrawer(self.poster)
        self.parser = create_parser()

    def test_validate_heatmap_center_with_invalid_center_string_raises_exception(self) -> None:
        invalid_centers = ["-10,0,10", "-10;10", "-10.10"]
        for invalid_center in invalid_centers:
            with self.subTest(f"{invalid_center}"):
                with self.assertRaises(ParameterError):
                    self.heatmap_drawer.validate_heatmap_center(invalid_center)

    def test_validate_heatmap_center_with_invalid_center_type_raises_exception(self) -> None:
        invalid_centers = ["A,B", "A,10", "-10,B"]
        for invalid_center in invalid_centers:
            with self.subTest(f"{invalid_center}"):
                with self.assertRaises(ParameterError):
                    self.heatmap_drawer.validate_heatmap_center(invalid_center)

    def test_validate_heatmap_center_with_invalid_center_values_raises_exception(self) -> None:
        invalid_centers = ["-91, 10", "-90, -181", "91, 10", "-91, 181", "-91, -181"]
        for invalid_center in invalid_centers:
            with self.subTest(f"{invalid_center}"):
                with self.assertRaises(ParameterError):
                    self.heatmap_drawer.validate_heatmap_center(invalid_center)

    def test_validate_heatmap_center_with_valid_center_returns_center(self) -> None:
        valid_centers = [
            ("-10, 10", s2sphere.LatLng.from_degrees(-10, 10)),
            ("-10,10", s2sphere.LatLng.from_degrees(-10, 10)),
            (" -10, 10 ", s2sphere.LatLng.from_degrees(-10, 10)),
            ("-90, -180", s2sphere.LatLng.from_degrees(-90, -180)),
            ("90, 180", s2sphere.LatLng.from_degrees(90, 180)),
            ("0, 0", s2sphere.LatLng.from_degrees(0, 0)),
        ]
        for valid_center, expected_result in valid_centers:
            with self.subTest(f"{valid_center} -> {expected_result}"):
                self.assertEqual(expected_result, self.heatmap_drawer.validate_heatmap_center(valid_center))

    def test_validate_heatmap_radius_with_invalid_value_raises_exception(self) -> None:
        with self.assertRaises(ParameterError):
            self.heatmap_drawer.validate_heatmap_radius(-10.0)

    def test_validate_heatmap_radius_without_center_raises_exception(self) -> None:
        with self.assertRaises(ParameterError):
            self.assertIsNone(self.heatmap_drawer._center)  # pylint: disable=protected-access
            self.heatmap_drawer.validate_heatmap_radius(10.0)

    def test_validate_heatmap_radius_with_valid_radius_returns_radius(self) -> None:
        valid_radii = [(0.1, 0.1), (10.0, 10.0)]
        for valid_radius, expected_result in valid_radii:
            with self.subTest(f"{valid_radius} -> {expected_result}"):
                self.heatmap_drawer.validate_heatmap_center("-10,10")
                self.assertEqual(expected_result, self.heatmap_drawer.validate_heatmap_radius(valid_radius))

    def test_validate_heatmap_line_width_with_invalid_string_raises_exception(self) -> None:
        invalid_strings = [
            "0.1,5.0, 0.2,2.0",
            "0.1,5.0, 0.2,2.0, 1.0,0.3, 0.1, 0.3",
        ]
        for invalid_string in invalid_strings:
            with self.subTest(f"{invalid_string}"):
                with self.assertRaises(ParameterError):
                    self.heatmap_drawer.validate_heatmap_line_width(invalid_string)

    def test_validate_heatmap_line_width_with_invalid_value_raises_exception(self) -> None:
        invalid_strings = [
            "1.1,5.0, 0.2,2.0, 1.0,0.3",
            "0.1,5.0, 1.1,2.0, 1.0,0.3",
            "0.1,5.0, 0.2,2.0, 1.1,0.3",
        ]
        for invalid_string in invalid_strings:
            with self.subTest(f"{invalid_string}"):
                with self.assertRaises(ParameterError):
                    self.heatmap_drawer.validate_heatmap_line_width(invalid_string)

    def test_validate_heatmap_line_width_with_valid_value_returns_line_widths(self) -> None:
        valid_strings = [
            ("automatic", None),
            ("AUTOMATIC", None),
            ("0.1,5.0, 0.2,2.0, 1.0,0.3", [(0.1, 5.0), (0.2, 2.0), (1.0, 0.3)]),
        ]
        for valid_string, expected_result in valid_strings:
            with self.subTest(f"{valid_string} -> {expected_result}"):
                self.assertEqual(expected_result, self.heatmap_drawer.validate_heatmap_line_width(valid_string))

    def test_validate_heatmap_line_width_without_value_returns_none(self) -> None:
        self.assertIsNone(self.heatmap_drawer.validate_heatmap_line_width())
        self.assertIsNone(self.heatmap_drawer.validate_heatmap_line_width(None))

    def test_get_line_transparencies_and_widths_with_values_returns_values(self) -> None:
        valid_strings = [
            ("0.1,5.0, 0.2,2.0, 1.0,0.3", [(0.1, 5.0), (0.2, 2.0), (1.0, 0.3)]),
            ("0.1,5.0,0.2,2.0,1.0,0.3", [(0.1, 5.0), (0.2, 2.0), (1.0, 0.3)]),
            (" 0.1,5.0, 0.2,2.0, 1.0,0.3 ", [(0.1, 5.0), (0.2, 2.0), (1.0, 0.3)]),
        ]
        for valid_string, expected_result in valid_strings:
            with self.subTest(f"{valid_string} -> {expected_result}"):
                self.assertEqual(expected_result, self.heatmap_drawer.validate_heatmap_line_width(valid_string))

    def test_get_line_transparencies_and_widths_with_automatic_returns_calculated_values(self) -> None:
        test_values = {
            "freiburg_newyork_6244.7km_larger_max_distance": (
                (47.99472, 7.84972),
                (40.7306, -73.9866),
                [(0.02, 0.5), (0.05, 0.2), (1.0, 0.05)],
            ),
            "berlin_paris_884km": (
                (52.51944, 13.40667),
                (48.725823, 2.372662),
                [(0.028383, 0.971593), (0.065719, 0.388637), (1.000000, 0.076199)],
            ),
            "amsterdam_paris_431.4km": (
                (52.378000, 4.900000),
                (48.859489, 2.320582),
                [(0.065106, 3.037229), (0.134574, 1.214891), (1.000000, 0.190957)],
            ),
            "amsterdam_brussels_174.4km": (
                (52.378, 4.90000),
                (50.8467, 4.3547),
                [(0.085898, 4.206781), (0.173559, 1.682712), (1.000000, 0.255932)],
            ),
            "amsterdam_rotterdam_57.9km": (
                (52.378, 4.90000),
                (51.950, 4.41667),
                [(0.095314, 4.736450), (0.191215, 1.894580), (1.000000, 0.285358)],
            ),
            "dortmund_gelsenkirchen_25.3km": (
                (51.51389, 7.46528),
                (51.51667, 7.10000),
                [(0.097950, 4.884733), (0.196157, 1.953893), (1.000000, 0.293596)],
            ),
            "hoofddorp_shiphol_6.6km_smaller_min_distance": (
                (52.3, 4.66667),
                (52.30857425000001, 4.76293775),
                [(0.1, 5.0), (0.2, 2.0), (1.0, 0.3)],
            ),
        }
        for _, test_value in test_values.items():
            bbox = s2sphere.sphere.LatLngRect.from_point_pair(
                s2sphere.LatLng.from_degrees(test_value[0][0], test_value[0][1]),
                s2sphere.LatLng.from_degrees(test_value[1][0], test_value[1][1]),
            )
            result = self.heatmap_drawer.get_line_transparencies_and_widths(bbox)
            expected_result = test_value[2]
            for pair in [0, 2]:
                for value in [0, 1]:
                    with self.subTest(f"{pair}|{value} -> {expected_result[pair][value]}"):
                        self.assertAlmostEqual(expected_result[pair][value], result[pair][value], 4)

    def test_parser_with_type_heatmap_sets_type(self) -> None:
        self.heatmap_drawer.create_args(self.parser)
        parsed = parse_args(self.parser, ["--type", "heatmap"])
        self.assertTrue(parsed.type)
        self.assertEqual(parsed.type, "heatmap")

    def test_parser_without_center_sets_none(self) -> None:
        self.heatmap_drawer.create_args(self.parser)
        parsed = self.parser.parse_args(["--type", "heatmap"])
        self.assertIsNone(parsed.heatmap_center)

    def test_parser_with_center_sets_float_value(self) -> None:
        self.heatmap_drawer.create_args(self.parser)
        lat_lng = "47.99472, 7.84972"
        parsed = self.parser.parse_args(["--type", "heatmap", "--heatmap-center", lat_lng])
        self.assertTrue(parsed.heatmap_center)
        self.assertEqual(parsed.heatmap_center, lat_lng)

    def test_parser_without_radius_sets_none(self) -> None:
        self.heatmap_drawer.create_args(self.parser)
        parsed = self.parser.parse_args(["--type", "heatmap"])
        self.assertIsNone(parsed.heatmap_radius)

    def test_parser_with_radius_sets_float_value(self) -> None:
        self.heatmap_drawer.create_args(self.parser)
        parsed = self.parser.parse_args(["--type", "heatmap", "--heatmap-radius", "10.0"])
        self.assertTrue(parsed.heatmap_radius)
        self.assertEqual(parsed.heatmap_radius, 10.0)

    def get_line_transparencies_and_widths_with_predefined_values_returns_predefined_values(self) -> None:
        self.heatmap_drawer.create_args(self.parser)
        line_width = "0.2,4.0, 0.3,3.0, 1.0,1.0"
        expected_line_width = [(0.2, 4.0), (0.3, 3.0), (1.0, 1.0)]
        parsed = self.parser.parse_args(
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
        self.heatmap_drawer.fetch_args(parsed)
        test_values = {
            "freiburg_newyork_6244.7km_larger_max_distance": (
                (47.99472, 7.84972),
                (40.7306, -73.9866),
            ),
            "hoofddorp_shiphol_6.6km_smaller_min_distance": (
                (52.3, 4.66667),
                (52.30857425000001, 4.76293775),
            ),
        }
        self.assertTrue(parsed.heatmap_center)
        self.assertTrue(parsed.heatmap_radius)
        for _, test_value in test_values.items():
            bbox = s2sphere.sphere.LatLngRect.from_point_pair(
                s2sphere.LatLng.from_degrees(test_value[0][0], test_value[0][1]),
                s2sphere.LatLng.from_degrees(test_value[1][0], test_value[1][1]),
            )
            with self.subTest(f"{line_width} -> {expected_line_width}"):
                self.assertTrue(parsed.heatmap_line_width)
                self.assertEqual(line_width, parsed.heatmap_line_width)
                self.assertEqual(expected_line_width, self.heatmap_drawer.get_line_transparencies_and_widths(bbox))
                self.assertEqual(
                    expected_line_width, self.heatmap_drawer._heatmap_line_width  # pylint: disable=protected-access
                )


if __name__ == "__main__":
    unittest.main()
