"""
ConfTest
"""
# Copyright 2022-2023 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import datetime
import os
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock

import pytest
import s2sphere  # type: ignore
from pytest_mock import MockerFixture

from gpxtrackposter.calendar_drawer import CalendarDrawer
from gpxtrackposter.circular_drawer import CircularDrawer
from gpxtrackposter.cli import create_parser
from gpxtrackposter.github_drawer import GithubDrawer
from gpxtrackposter.grid_drawer import GridDrawer
from gpxtrackposter.heatmap_drawer import HeatmapDrawer
from gpxtrackposter.poster import Poster
from gpxtrackposter.units import Units


@pytest.fixture(scope="session", autouse=True)
def clear_files_teardown() -> Generator:
    """Session tear down"""
    yield None
    try:
        os.remove("logger.log")
    except FileNotFoundError:
        pass


@pytest.fixture(name="default_values")
def fixture_default_values() -> Namespace:
    """Return default values as argparse.Namespace"""
    arguments = Namespace(
        gpx_dir=".",
        output="poster.svg",
        language="",
        localedir=None,
        year="all",
        athlete="John Doe",
        title=None,
        special=[],
        type="grid",
        background_color="#222222",
        track_color="#4DD2FF",
        track_color2=None,
        text_color="#FFFFFF",
        special_color="#FFFF00",
        special_color2=None,
        units="metric",
        clear_cache=False,
        verbose=False,
        special_distance=10.0,
        special_distance2=20.0,
        min_distance=1.0,
        activity_type="all",
        with_animation=False,
        animation_time=30,
        workers=None,
    )
    return arguments


@pytest.fixture(name="mock_track_instance")
def fixture_mock_track_instance(mocker: MockerFixture) -> MagicMock:
    """Fixture for Track"""
    mock_track_class = mocker.patch("gpxtrackposter.track_loader.Track")
    instance = mock_track_class.return_value
    instance.length.return_value = 1 * Units().km
    instance.start_time.return_value = datetime.datetime.now()
    instance.end_time.return_value = datetime.datetime.now()
    return instance


@pytest.fixture(name="mock_track_instance_berlin_paris")
def fixture_mock_track_instance_berlin_paris(mocker: MockerFixture) -> MagicMock:
    """Fixture for Track 1 - berlin-paris 884km"""
    mock_track_class = mocker.patch("gpxtrackposter.track_loader.Track")
    instance = mock_track_class.return_value
    instance.length.return_value = 884.0 * Units().km
    instance.start_time.return_value = datetime.datetime.now()
    instance.end_time.return_value = datetime.datetime.now()
    instance.bbox.return_value = s2sphere.sphere.LatLngRect.from_point_pair(
        s2sphere.LatLng.from_degrees(52.51944, 13.40667),
        s2sphere.LatLng.from_degrees(48.725823, 2.372662),
    )
    return instance


@pytest.fixture(name="mock_track_instance_amsterdam_paris")
def fixture_mock_track_instance_amsterdam_paris(mocker: MockerFixture) -> MagicMock:
    """Fixture for Track 2 - amsterdam-paris 431.4km"""
    mock_track_class = mocker.patch("gpxtrackposter.track_loader.Track")
    instance = mock_track_class.return_value
    instance.length.return_value = 431.4 * Units().km
    instance.start_time.return_value = datetime.datetime.now()
    instance.end_time.return_value = datetime.datetime.now()
    instance.bbox.return_value = s2sphere.sphere.LatLngRect.from_point_pair(
        s2sphere.LatLng.from_degrees(52.378000, 4.900000),
        s2sphere.LatLng.from_degrees(48.859489, 2.320582),
    )
    return instance


@pytest.fixture(name="parser")
def fixture_parser() -> ArgumentParser:
    """Return an ArgParser"""
    return create_parser()


@pytest.fixture(name="poster")
def fixture_poster() -> Poster:
    """Fixture for Poster with default values"""
    poster = Poster()
    poster.units = "metric"
    poster.colors = {
        "background": "#222222",
        "text": "#FFFFFF",
        "special": "#FFFF00",
        "track": "#4DD2FF",
        "track2": poster.colors["track"],
        "special2": poster.colors["special"],
    }
    poster.special_distance = {"special_distance": 10.0 * Units().km, "special_distance2": 20.0 * Units().km}
    poster.width = 200
    poster.height = 300
    poster.tracks_drawer = None
    poster.with_animation = False
    poster.animation_time = 30
    poster.set_language(None, None)
    return poster


@pytest.fixture(name="calendar_drawer")
def fixture_calendar_drawer() -> CalendarDrawer:
    """Return a CalendarDrawer"""
    return CalendarDrawer(Poster())


@pytest.fixture(name="circular_drawer")
def fixture_circular_drawer() -> CircularDrawer:
    """Return a CircularDrawer"""
    return CircularDrawer(Poster())


@pytest.fixture(name="github_drawer")
def fixture_github_drawer() -> GithubDrawer:
    """Return a GithubDrawer"""
    return GithubDrawer(Poster())


@pytest.fixture(name="grid_drawer")
def fixture_grid_drawer() -> GridDrawer:
    """Return a GridDrawer"""
    return GridDrawer(Poster())


@pytest.fixture(name="heatmap_drawer")
def fixture_heatmap_drawer() -> HeatmapDrawer:
    """Return a HeatmapDrawer"""
    return HeatmapDrawer(Poster())


@pytest.fixture(scope="session", name="gpx_file_track_no_length_content")
def fixture_gpx_file_track_no_length_content() -> str:
    """Temporary gpx file - no length content"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1"
     xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"
     version="1.1" creator="MapSource 6.16.3">
  <metadata>
    <time>2022-01-01T12:00:00Z</time>
    <bounds minlat="52.516495" maxlat="52.517761" minlon="13.377094" maxlon="13.377587">
    </bounds>
  </metadata>
  <trk>
    <name>track1</name>
    <trkseg>
      <trkpt lat="52.517761" lon="13.377094">
        <time>2022-01-01T12:00:00Z</time>
      </trkpt>
      <trkpt lat="52.517761" lon="13.377094">
        <time>2022-01-01T12:01:00Z</time>
      </trkpt>
    </trkseg>
  </trk>
</gpx>
"""


@pytest.fixture(scope="session", name="gpx_file_track_hike_content")
def fixture_gpx_file_track_hike_content() -> str:
    """gpx file content - track hike content, 1.3km"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1"
     xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"
     version="1.1" creator="MapSource 6.16.3">
  <metadata>
    <time>2021-01-01T12:00:00Z</time>
    <bounds minlat="52.515947" maxlat="52.517703" minlon="13.370029" maxlon="13.380634">
    </bounds>
  </metadata>
  <trk>
    <name>Track Hike</name>
    <type>Hike</type>
    <trkseg>
      <trkpt lat="52.516495" lon="13.377587">
        <time>2021-01-01T12:00:00Z</time>
      </trkpt>
      <trkpt lat="52.517761" lon="13.377094">
        <time>2021-01-01T12:01:00Z</time>
      </trkpt>
      <trkpt lat="52.517703" lon="13.370908">
        <time>2021-01-02T12:02:00Z</time>
      </trkpt>
      <trkpt lat="52.515947" lon="13.370029">
        <time>2021-01-02T12:03:00Z</time>
      </trkpt>
      <trkpt lat="52.516495" lon="13.377587">
        <time>2021-01-02T12:04:00Z</time>
      </trkpt>
    </trkseg>
  </trk>
</gpx>
"""


@pytest.fixture(scope="session", name="gpx_file_track_walk_content")
def fixture_gpx_file_track_walk_content() -> str:
    """gpx file content - track walk content, 0.7km"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1"
     xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"
     version="1.1" creator="MapSource 6.16.3">
  <metadata>
    <time>2021-01-01T12:30:00Z</time>
    <bounds minlat="52.516495" maxlat="52.517959" minlon="13.377094" maxlon="13.380634">
    </bounds>
  </metadata>
  <trk>
    <name>Track Walk</name>
    <type>Walk</type>
    <trkseg>
      <trkpt lat="52.517761" lon="13.377094">
        <time>2021-01-01T12:30:00Z</time>
      </trkpt>
      <trkpt lat="52.516495" lon="13.377587">
        <time>2021-01-01T12:31:00Z</time>
      </trkpt>
      <trkpt lat="52.516665" lon="13.380634">
        <time>2021-01-01T12:32:00Z</time>
      </trkpt>
      <trkpt lat="52.517959" lon="13.380312">
        <time>2021-01-01T12:33:00Z</time>
      </trkpt>
      <trkpt lat="52.517761" lon="13.377094">
        <time>2021-01-01T12:34:00Z</time>
      </trkpt>
    </trkseg>
  </trk>
</gpx>
"""


@pytest.fixture(scope="session", name="gpx_file_track_no_type_content")
def fixture_gpx_file_track_no_type_content() -> str:
    """gpx file content - track no type content, 0.8km"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1"
     xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"
     version="1.1" creator="MapSource 6.16.3">
  <metadata>
    <time>2022-01-02T12:00:00Z</time>
    <bounds minlat="52.514732" maxlat="52.516665" minlon="13.377587" maxlon="13.380634">
    </bounds>
  </metadata>
  <trk>
    <name>Track no type</name>
    <trkseg>
      <trkpt lat="52.516495" lon="13.377587">
        <time>2022-01-02T12:00:00Z</time>
      </trkpt>
      <trkpt lat="52.514732" lon="13.377689">
        <time>2022-01-02T12:01:00Z</time>
      </trkpt>
      <trkpt lat="52.515202" lon="13.381337">
        <time>2022-01-02T12:02:00Z</time>
      </trkpt>
      <trkpt lat="52.516665" lon="13.380634">
        <time>2022-01-02T12:03:00Z</time>
      </trkpt>
      <trkpt lat="52.516495" lon="13.377587">
        <time>2022-01-02T12:04:00Z</time>
      </trkpt>
    </trkseg>
  </trk>
</gpx>
"""


@pytest.fixture(scope="session", name="gpx_file_empty")
def fixture_gpx_file_empty(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Temporary gpx file - empty"""
    gpx_file_empty = tmp_path_factory.mktemp("data") / "gpx_file_empty.gpx"
    gpx_file_empty.write_text("")
    return gpx_file_empty


@pytest.fixture(scope="session", name="gpx_file_invalid")
def fixture_gpx_file_invalid(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Temporary gpx file - invalid"""
    gpx_file_invalid = tmp_path_factory.mktemp("data") / "gpx_file_invalid.gpx"
    gpx_file_invalid.write_text("<xml>")
    return gpx_file_invalid


@pytest.fixture(scope="session", name="gpx_file_no_permission")
def fixture_gpx_file_no_permission(tmp_path_factory: pytest.TempPathFactory, gpx_file_track_walk_content: str) -> Path:
    """Temporary gpx file - no permission"""
    gpx_file_no_permission = tmp_path_factory.mktemp("data") / "gpx_file_no_permission.gpx"
    gpx_file_no_permission.write_text(gpx_file_track_walk_content)
    os.chmod(gpx_file_no_permission, 0000)
    return gpx_file_no_permission


@pytest.fixture(scope="session", name="gpx_file_track_no_length")
def fixture_gpx_file_track_no_length(
    tmp_path_factory: pytest.TempPathFactory, gpx_file_track_no_length_content: str
) -> Path:
    """Temporary gpx file - no length"""
    gpx_file_track_no_length = tmp_path_factory.mktemp("data") / "gpx_file_track_no_length.gpx"
    gpx_file_track_no_length.write_text(gpx_file_track_no_length_content)
    return gpx_file_track_no_length


@pytest.fixture(scope="session", name="gpx_file_track_hike")
def fixture_gpx_file_track_hike(tmp_path_factory: pytest.TempPathFactory, gpx_file_track_hike_content: str) -> Path:
    """Temporary gpx file - track hike"""
    gpx_file_track_hike = tmp_path_factory.mktemp("data") / "gpx_file_track_hike.gpx"
    gpx_file_track_hike.write_text(gpx_file_track_hike_content)
    return gpx_file_track_hike


@pytest.fixture(scope="session", name="gpx_file_track_walk")
def fixture_gpx_file_track_walk(tmp_path_factory: pytest.TempPathFactory, gpx_file_track_walk_content: str) -> Path:
    """Temporary gpx file - track walk"""
    gpx_file_track_walk = tmp_path_factory.mktemp("data") / "gpx_file_track_walk.gpx"
    gpx_file_track_walk.write_text(gpx_file_track_walk_content)
    return gpx_file_track_walk


@pytest.fixture(scope="session", name="gpx_file_track_no_type")
def fixture_gpx_file_track_no_type(
    tmp_path_factory: pytest.TempPathFactory, gpx_file_track_no_type_content: str
) -> Path:
    """Temporary gpx file - track no type"""
    gpx_file_track_no_type = tmp_path_factory.mktemp("data") / "gpx_file_track_no_type.gpx"
    gpx_file_track_no_type.write_text(gpx_file_track_no_type_content)
    return gpx_file_track_no_type


@pytest.fixture(scope="session", name="gpx_dir_with_tracks")
def fixture_gpx_dir_with_tracks(
    tmp_path_factory: pytest.TempPathFactory,
    gpx_file_track_hike_content: str,
    gpx_file_track_walk_content: str,
    gpx_file_track_no_type_content: str,
) -> Path:
    """Temporary gpx directory - with tracks"""
    gpx_dir_with_tracks = tmp_path_factory.mktemp("data")
    gpx_file_track_hike = gpx_dir_with_tracks / "gpx_file_track_hike.gpx"
    gpx_file_track_hike.write_text(gpx_file_track_hike_content)
    gpx_file_track_walk = gpx_dir_with_tracks / "gpx_file_track_walk.gpx"
    gpx_file_track_walk.write_text(gpx_file_track_walk_content)
    gpx_file_track_no_type = gpx_dir_with_tracks / "gpx_file_track_no_type.gpx"
    gpx_file_track_no_type.write_text(gpx_file_track_no_type_content)
    file_to_be_skipped = gpx_dir_with_tracks / "file_to_be_skipped.txt"
    file_to_be_skipped.write_text("Something ...")
    return gpx_dir_with_tracks
