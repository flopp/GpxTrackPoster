"""Create a poster from track data."""
# Copyright 2016-2022 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import gettext
import locale
import logging
import typing
from collections import defaultdict

import pint  # type: ignore
import svgwrite  # type: ignore

from gpxtrackposter.quantity_range import QuantityRange
from gpxtrackposter.track import Track
from gpxtrackposter.units import Units
from gpxtrackposter.utils import format_float
from gpxtrackposter.xy import XY
from gpxtrackposter.year_range import YearRange

if typing.TYPE_CHECKING:
    # avoid circlic import
    from gpxtrackposter.tracks_drawer import TracksDrawer  # pylint: disable=cyclic-import

log = logging.getLogger(__name__)


class Poster:
    """Create a poster from track data.

    Attributes:
        _athlete: Name of athlete to be displayed on poster.
        _title: Title of poster.
        tracks_by_date: Tracks organized temporally if needed.
        tracks: List of tracks to be used in the poster.
        length_range: Range of lengths of tracks in poster.
        length_range_by_date: Range of lengths organized temporally.
        units: Length units to be used in poster.
        colors: Colors for various components of the poster.
        width: Poster width.
        height: Poster height.
        years: Years included in the poster.
        tracks_drawer: drawer used to draw the poster.

    Methods:
        set_tracks: Associate the Poster with a set of tracks
        draw: Draw the tracks on the poster.
        m2u: Convert meters to kilometers or miles based on units
        u: Return distance unit (km or mi)
    """

    def __init__(self) -> None:
        self._athlete: typing.Optional[str] = None
        self._title: typing.Optional[str] = None
        self.tracks_by_date: typing.Dict[str, typing.List[Track]] = defaultdict(list)
        self.year_tracks_date_count_dict: typing.Dict[int, int] = defaultdict(int)
        self.tracks: typing.List[Track] = []
        self.length_range = QuantityRange()
        self.length_range_by_date = QuantityRange()
        self.total_length_year_dict: typing.Dict[int, pint.quantity.Quantity] = defaultdict(int)  # type: ignore
        self.units = "metric"
        self.colors = {
            "background": "#222222",
            "text": "#FFFFFF",
            "special": "#FFFF00",
            "track": "#4DD2FF",
        }
        self.special_distance: typing.Dict[str, float] = {"special_distance1": 10, "special_distance2": 20}
        self.width = 200
        self.height = 300
        self.years = YearRange()
        self.tracks_drawer: typing.Optional["TracksDrawer"] = None
        self._trans: typing.Optional[typing.Callable[[str], str]] = None
        self.with_animation = False
        self.animation_time: int = 30
        self.set_language(None, None)

    def set_language(self, language: typing.Optional[str], localedir: typing.Optional[str]) -> None:
        if language:
            try:
                locale.setlocale(locale.LC_ALL, f"{language}.utf8")
            except locale.Error as e:
                log.warning("Unable to set the locale to %s (%s)", language, str(e))
                language = None

        # Fall-back to NullTranslations, if the specified language translation cannot be found.
        if language:
            lang = gettext.translation("gpxposter", localedir=localedir, languages=[language], fallback=True)
            if len(lang.info()) == 0:
                log.warning(
                    "Unable to load translations for %s from %s; falling back to the default translation.",
                    language,
                    localedir if localedir else "the system's default locale directory",
                )
        else:
            lang = gettext.NullTranslations()
        self._trans = lang.gettext

    def translate(self, s: str) -> str:
        if self._trans is None:
            return s
        return self._trans(s)

    def month_name(self, month: int) -> str:
        assert 1 <= month <= 12

        return [
            self.translate("January"),
            self.translate("February"),
            self.translate("March"),
            self.translate("April"),
            self.translate("May"),
            self.translate("June"),
            self.translate("July"),
            self.translate("August"),
            self.translate("September"),
            self.translate("October"),
            self.translate("November"),
            self.translate("December"),
        ][month - 1]

    def set_athlete(self, athlete: str) -> None:
        self._athlete = athlete

    def set_title(self, title: str) -> None:
        self._title = title

    def set_with_animation(self, with_animation: bool) -> None:
        self.with_animation = with_animation

    def set_animation_time(self, animation_time: int) -> None:
        self.animation_time = animation_time

    def set_tracks(self, tracks: typing.List[Track]) -> None:
        """Associate the set of tracks with this poster.

        In addition to setting self.tracks, also compute the necessary attributes for the Poster
        based on this set of tracks.
        """
        self.tracks = tracks
        self.tracks_by_date.clear()
        self.length_range.clear()
        self.length_range_by_date.clear()
        self.year_tracks_date_count_dict.clear()
        self._compute_years(tracks)
        for track in tracks:
            if not self.years.contains(track.start_time()):
                continue
            text_date = track.start_time().strftime("%Y-%m-%d")
            year = track.start_time().year
            if text_date not in self.tracks_by_date:
                self.year_tracks_date_count_dict[year] += 1
            self.tracks_by_date[text_date].append(track)
            self.length_range.extend(track.length())
        for date_tracks in self.tracks_by_date.values():
            length = pint.quantity.Quantity(sum([t.length() for t in date_tracks]))
            self.length_range_by_date.extend(length)

    def draw(self, drawer: "TracksDrawer", output: str) -> None:
        """Set the Poster's drawer and draw the tracks."""
        self.tracks_drawer = drawer
        d = svgwrite.Drawing(output, (f"{self.width}mm", f"{self.height}mm"))
        d.viewbox(width=self.width, height=self.height)
        d.add(d.rect((0, 0), (self.width, self.height), fill=self.colors["background"]))
        self._draw_header(d)
        self._draw_footer(d)
        self._draw_tracks(d, XY(self.width - 20, self.height - 30 - 30), XY(10, 30))
        d.save()

    def m2u(self, m: pint.quantity.Quantity) -> float:
        """Convert meters to kilometers or miles, according to units."""
        if self.units == "metric":
            return m.m_as(Units().km)
        return m.m_as(Units().mile)

    def u(self) -> str:
        """Return the unit of distance being used on the Poster."""
        if self.units == "metric":
            return self.translate("km")
        return self.translate("mi")

    def format_distance(self, d: pint.quantity.Quantity) -> str:
        """Formats a distance using the locale specific float format and the selected unit."""
        return format_float(self.m2u(d)) + " " + self.u()

    def _draw_tracks(self, d: svgwrite.Drawing, size: XY, offset: XY) -> None:
        assert self.tracks_drawer

        g = d.g(id="tracks")
        d.add(g)

        self.tracks_drawer.draw(d, g, size, offset)

    def _draw_header(self, d: svgwrite.Drawing) -> None:
        g = d.g(id="header")
        d.add(g)

        text_color = self.colors["text"]
        title_style = "font-size:12px; font-family:Arial; font-weight:bold;"
        assert self._title is not None
        g.add(d.text(self._title, insert=(10, 20), fill=text_color, style=title_style))

    def _draw_footer(self, d: svgwrite.Drawing) -> None:
        g = d.g(id="footer")
        d.add(g)

        text_color = self.colors["text"]
        header_style = "font-size:4px; font-family:Arial"
        value_style = "font-size:9px; font-family:Arial"
        small_value_style = "font-size:3px; font-family:Arial"

        (
            total_length,
            average_length,
            length_range,
            weeks,
        ) = self._compute_track_statistics()

        g.add(
            d.text(
                self.translate("ATHLETE"),
                insert=(10, self.height - 20),
                fill=text_color,
                style=header_style,
            )
        )
        g.add(
            d.text(
                self._athlete,
                insert=(10, self.height - 10),
                fill=text_color,
                style=value_style,
            )
        )
        g.add(
            d.text(
                self.translate("STATISTICS"),
                insert=(120, self.height - 20),
                fill=text_color,
                style=header_style,
            )
        )
        g.add(
            d.text(
                self.translate("Number") + f": {len(self.tracks)}",
                insert=(120, self.height - 15),
                fill=text_color,
                style=small_value_style,
            )
        )
        weekly = len(self.tracks) / weeks if weeks else 0.0
        g.add(
            d.text(
                self.translate("Weekly") + ": " + format_float(weekly),
                insert=(120, self.height - 10),
                fill=text_color,
                style=small_value_style,
            )
        )
        g.add(
            d.text(
                self.translate("Total") + ": " + self.format_distance(total_length),
                insert=(141, self.height - 15),
                fill=text_color,
                style=small_value_style,
            )
        )
        g.add(
            d.text(
                self.translate("Avg") + ": " + self.format_distance(average_length),
                insert=(141, self.height - 10),
                fill=text_color,
                style=small_value_style,
            )
        )
        if length_range.is_valid():
            min_length = length_range.lower()
            max_length = length_range.upper()
            assert min_length is not None
            assert max_length is not None
        else:
            min_length = pint.quantity.Quantity(0.0, "meter")
            max_length = pint.quantity.Quantity(0.0, "meter")
        g.add(
            d.text(
                self.translate("Min") + ": " + self.format_distance(min_length),
                insert=(167, self.height - 15),
                fill=text_color,
                style=small_value_style,
            )
        )
        g.add(
            d.text(
                self.translate("Max") + ": " + self.format_distance(max_length),
                insert=(167, self.height - 10),
                fill=text_color,
                style=small_value_style,
            )
        )

    def _compute_track_statistics(
        self,
    ) -> typing.Tuple[pint.quantity.Quantity, pint.quantity.Quantity, QuantityRange, int]:
        length_range = QuantityRange()
        total_length = 0.0 * Units().meter
        self.total_length_year_dict.clear()
        weeks = {}
        for t in self.tracks:
            total_length += t.length()
            self.total_length_year_dict[t.start_time().year] += t.length()
            length_range.extend(t.length())
            # time.isocalendar()[1] -> week number
            weeks[(t.start_time().year, t.start_time().isocalendar()[1])] = 1
        average_length = total_length / len(self.tracks) if self.tracks else 0.0 * Units().meter
        return (
            total_length,
            average_length,
            length_range,
            len(weeks),
        )

    def _compute_years(self, tracks: typing.List[Track]) -> None:
        self.years.clear()
        for t in tracks:
            self.years.add(t.start_time())
