"""Draw a heatmap poster."""
# Copyright 2016-2023 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import argparse
import logging
import math
from typing import Dict, List, Optional, Tuple

import s2sphere  # type: ignore
import svgwrite  # type: ignore
from geopy.distance import distance  # type: ignore

from gpxtrackposter import utils
from gpxtrackposter.exceptions import ParameterError, PosterError
from gpxtrackposter.poster import Poster
from gpxtrackposter.tracks_drawer import TracksDrawer
from gpxtrackposter.xy import XY

log = logging.getLogger(__name__)


class HeatmapDrawer(TracksDrawer):
    """Draw a heatmap Poster based on the tracks.

    Attributes:
        _center: Center of the heatmap.
        _radius: Scale the heatmap so that a circle with radius (in KM) is visible.

    Methods:
        create_args: Create arguments for heatmap.
        fetch_args: Get arguments passed.
        draw: Draw the heatmap based on the Poster's tracks.

    """

    def __init__(self, the_poster: Poster):
        super().__init__(the_poster)
        self._center: Optional[s2sphere.LatLng] = None
        self._radius: Optional[float] = None
        self._heatmap_line_width_low: float = 10.0
        self._heatmap_line_width_upp: float = 1000.0
        self._heatmap_line_width_lower: List[Tuple[float, float]] = [(0.10, 5.0), (0.20, 2.0), (1.0, 0.30)]
        self._heatmap_line_width_upper: List[Tuple[float, float]] = [(0.02, 0.5), (0.05, 0.2), (1.0, 0.05)]
        self._heatmap_line_width: Optional[List[Tuple[float, float]]] = None

    def create_args(self, args_parser: argparse.ArgumentParser) -> None:
        """Add arguments to the parser"""
        group = args_parser.add_argument_group("Heatmap Type Options")
        group.add_argument(
            "--heatmap-center",
            dest="heatmap_center",
            metavar="LAT,LNG",
            type=str,
            help="Center of the heatmap (default: automatic).",
        )
        group.add_argument(
            "--heatmap-radius",
            dest="heatmap_radius",
            metavar="RADIUS_KM",
            type=float,
            help="Scale the heatmap such that at least a circle with radius=RADIUS_KM is visible "
            "(default: automatic).",
        )
        group.add_argument(
            "--heatmap-line-transparency-width",
            dest="heatmap_line_width",
            metavar="TRANSP_1,WIDTH_1, TRANSP_2,WIDTH_2, TRANSP_3,WIDTH_3",
            type=str,
            help="Define three transparency and width tuples for the heatmap lines or set it to "
            "`automatic` for automatic calculation (default: 0.1,5.0, 0.2,2.0, 1.0,0.3).",
        )

    # pylint: disable=too-many-branches
    def fetch_args(self, args: argparse.Namespace) -> None:
        """Get arguments that were passed, and also perform basic validation on them.

        For example, make sure the center is an actual lat, lng , and make sure the radius is a
        positive number. Also, if radius is passed, then center must also be passed.

        Raises:
            ParameterError: Center was not a valid lat, lng coordinate, or radius was not positive.
            ParameterError: Line transparency and width values are not valid
        """
        self._center = self.validate_heatmap_center(args.heatmap_center)
        self._radius = self.validate_heatmap_radius(args.heatmap_radius)
        self._heatmap_line_width = self.validate_heatmap_line_width(args.heatmap_line_width)

    def get_line_transparencies_and_widths(self, bbox: s2sphere.sphere.LatLngRect) -> List[Tuple[float, float]]:
        """Get a tuple of line widths and transparencies"""
        if self._heatmap_line_width:
            return self._heatmap_line_width
        # automatic calculation of line transparencies and widths
        low = self._heatmap_line_width_low
        upp = self._heatmap_line_width_upp
        lower = self._heatmap_line_width_lower
        upper = self._heatmap_line_width_upper
        d = distance(
            (bbox.lo().lat().degrees, bbox.lo().lng().degrees), (bbox.hi().lat().degrees, bbox.hi().lng().degrees)
        ).km
        log.info("Length of diagonal of boundary box %s", str(d))
        if d > upp:
            return upper
        if d < low:
            return lower
        return [
            (
                lower[0][0] + d / (upp - low) * (upper[0][0] - lower[0][0]),
                (lower[0][1] + d / (upp - low) * (upper[0][1] - lower[0][1])),
            ),
            (
                lower[1][0] + d / (upp - low) * (upper[1][0] - lower[1][0]),
                (lower[1][1] + d / (upp - low) * (upper[1][1] - lower[1][1])),
            ),
            (
                lower[2][0] + d / (upp - low) * (upper[2][0] - lower[2][0]),
                (lower[2][1] + d / (upp - low) * (upper[2][1] - lower[2][1])),
            ),
        ]

    def _determine_bbox(self) -> s2sphere.LatLngRect:
        if self._center:
            log.info("Forcing heatmap center to %s", str(self._center))
            dlat, dlng = 0.0, 0.0
            if self._radius:
                er = 6378.1
                quarter = er * math.pi / 2
                dlat = 90 * self._radius / quarter
                scale = 1 / math.cos(self._center.lat().radians)
                dlng = scale * 90 * self._radius / quarter
            else:
                for tr in self.poster.tracks:
                    for line in tr.polylines:
                        for latlng in line:
                            d = abs(self._center.lat().degrees - latlng.lat().degrees)
                            dlat = max(dlat, d)
                            d = abs(self._center.lng().degrees - latlng.lng().degrees)
                            while d > 360:
                                d -= 360
                            if d > 180:
                                d = 360 - d
                            dlng = max(dlng, d)
            return s2sphere.LatLngRect.from_center_size(self._center, s2sphere.LatLng.from_degrees(2 * dlat, 2 * dlng))

        tracks_bbox = s2sphere.LatLngRect()
        for tr in self.poster.tracks:
            tracks_bbox = tracks_bbox.union(tr.bbox())
        return tracks_bbox

    def draw(self, dr: svgwrite.Drawing, g: svgwrite.container.Group, size: XY, offset: XY) -> None:
        """Draw the heatmap based on tracks."""
        if len(self.poster.tracks) == 0:
            raise PosterError("No tracks to draw.")
        bbox = self._determine_bbox()
        line_transparencies_and_widths = self.get_line_transparencies_and_widths(bbox)
        year_groups: Dict[int, svgwrite.container.Group] = {}
        for tr in self.poster.tracks:
            year = tr.start_time().year
            if year not in year_groups:
                g_year = dr.g(id=f"year{year}")
                g.add(g_year)
                year_groups[year] = g_year
            else:
                g_year = year_groups[year]
            color = self.color(self.poster.length_range, tr.length(), tr.special)
            for line in utils.project(bbox, size, offset, tr.polylines):
                for opacity, width in line_transparencies_and_widths:
                    g_year.add(
                        dr.polyline(
                            points=line,
                            stroke=color,
                            stroke_opacity=opacity,
                            fill="none",
                            stroke_width=width,
                            stroke_linejoin="round",
                            stroke_linecap="round",
                        )
                    )

    def validate_heatmap_center(self, heatmap_center: str = None) -> s2sphere.LatLng:
        """Validate and return the Heatmap center."""
        if heatmap_center:
            latlng_str = heatmap_center.split(",")
            if len(latlng_str) != 2:
                raise ParameterError(f"Not a valid LAT,LNG pair: {heatmap_center}")
            try:
                lat = float(latlng_str[0].strip())
                lng = float(latlng_str[1].strip())
            except ValueError as e:
                raise ParameterError(f"Not a valid LAT,LNG pair: {heatmap_center}") from e
            if not -90 <= lat <= 90 or not -180 <= lng <= 180:
                raise ParameterError(f"Not a valid LAT,LNG pair: {heatmap_center}")
            self._center = s2sphere.LatLng.from_degrees(lat, lng)
        return self._center

    def validate_heatmap_radius(self, heatmap_radius: float = None) -> Optional[float]:
        """Validate and return the Heatmap radius."""
        if heatmap_radius:
            if heatmap_radius <= 0:
                raise ParameterError(f"Not a valid radius: {heatmap_radius} (must be > 0)")
            if not self._center:
                raise ParameterError("--heatmap-radius needs --heatmap-center")
            self._radius = heatmap_radius
        return self._radius

    def validate_heatmap_line_width(self, heatmap_line_width: str = None) -> Optional[List[Tuple[float, float]]]:
        """Validate and return a tuple of the Heatmap line widths."""
        if heatmap_line_width:
            if heatmap_line_width.lower() == "automatic":
                self._heatmap_line_width = None
            else:
                trans_width_str = heatmap_line_width.split(",")
                if len(trans_width_str) != 6:
                    raise ParameterError(f"Not three valid TRANSPARENCY,WIDTH pairs: {heatmap_line_width}")
                try:
                    self._heatmap_line_width = []
                    for value in range(0, 5, 2):
                        transparency = float(trans_width_str[value].strip())
                        width = float(trans_width_str[value + 1].strip())
                        if transparency < 0 or transparency > 1:
                            raise ParameterError(
                                f"Not a valid TRANSPARENCY value (0 < value < 1): {transparency} in "
                                f"{heatmap_line_width}"
                            )
                        self._heatmap_line_width.append((transparency, width))
                except ValueError as e:
                    raise ParameterError(f"Not three valid TRANSPARENCY,WIDTH pairs: {heatmap_line_width}") from e
            return self._heatmap_line_width
        return None
