![CI](https://github.com/flopp/GpxTrackPoster/workflows/CI/badge.svg)
[![Format](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
![License MIT](https://img.shields.io/badge/license-MIT-lightgrey.svg?style=flat)

# GpxTrackPoster
Create a visually appealing poster from your GPX tracks - heavily inspired by https://www.instagram.com/p/Behppx9HCfx/

## Setup
1. Clone the repository: `git clone https://github.com/flopp/GpxTrackPoster.git`
2. `cd GpxTrackPoster`
3. Create virtualenv: `virtualenv -p /usr/bin/python3 venv` or `python -m venv venv`
4. Activate virtualenv: `source venv/bin/activate`
5. Install the package: `pip install .`
6. Install development requirements (only if you want to contribute code!): `pip install -r requirements-dev.txt`
7. Run `create_poster` (see above)
8. Deactivate virtualenv: `deactivate`

### Container
There is a Dockerfile in this repository, which you can use to run this software.
1. Build the container: `podman build -f Dockerfile -t gpxtrackposter:latest`
2. Run the container to build your poster: `podman run --rm -v /my/gpx/files:/gpx --name gpxtrackposter localhost/gpxtrackposter:latest  create_poster --gpx-dir /gpx --output /gpx/poster.svg`

## Usage
First of all, you need directory with a bunch of GPX files (e.g. you can export all your tracks from Garmin Connect with the excellent tool [garmin-connect-export](https://github.com/kjkjava/garmin-connect-export), or use [StravaExportToGPX](https://github.com/flopp/StravaExportToGPX), or use [runtastic](https://github.com/yihong0618/Runtastic), or use [nrc-exporter](https://github.com/yasoob/nrc-exporter) to convert the activities in a Strava or Runtastic or `Nike Run Club` export zip file to GPX or GPX files).

You will need a little experience running things from the command line to use this script. That said, here are the usage details from the `--help` flag:

Get data from strava is ok now:
```
create_poster --from-strava strava.json --year 2020 --title "Running" \
    --athlete "Florian Pigorsch" --special 4110886680(strava id)
```
Only you need is change the strava config
[How to get strava config](https://developers.strava.com/docs/getting-started/)

```
usage: create_poster [-h] [--gpx-dir DIR] [--output FILE]
                     [--language LANGUAGE] [--localedir DIR] [--year YEAR]
                     [--title TITLE] [--athlete NAME] [--special FILE]
                     [--type TYPE] [--background-color COLOR]
                     [--track-color COLOR] [--track-color2 COLOR]
                     [--text-color COLOR] [--special-color COLOR]
                     [--special-color2 COLOR] [--units UNITS] [--clear-cache]
                     [--workers NUMBER_OF_WORKERS] [--from-strava FILE]
                     [--verbose] [--logfile FILE]
                     [--special-distance DISTANCE]
                     [--special-distance2 DISTANCE] [--min-distance DISTANCE]
                     [--activity-type ACTIVITY_TYPE] [--with-animation]
                     [--animation-time ANIMATION_TIME]
                     [--heatmap-center LAT,LNG] [--heatmap-radius RADIUS_KM]
                     [--heatmap-line-transparency-width TRANSP_1,WIDTH_1, TRANSP_2,WIDTH_2, TRANSP_3,WIDTH_3]
                     [--circular-rings] [--circular-ring-color COLOR]
                     [--circular-ring-max-distance DISTANCE]

optional arguments:
  -h, --help            show this help message and exit
  --gpx-dir DIR         Directory containing GPX files (default: current
                        directory).
  --output FILE         Name of generated SVG image file (default:
                        "poster.svg").
  --language LANGUAGE   Language (default: english).
  --localedir DIR       The directory where the translation files can be found
                        (default: the system's locale directory).
  --year YEAR           Filter tracks by year; "NUM", "NUM-NUM", "all"
                        (default: all years)
  --title TITLE         Title to display.
  --athlete NAME        Athlete name to display (default: "John Doe").
  --special FILE        Mark track file from the GPX directory as special; use
                        multiple times to mark multiple tracks.
  --type TYPE           Type of poster to create (default: "grid", available:
                        "grid", "calendar", "heatmap", "circular", "github").
  --background-color COLOR
                        Background color of poster (default: "#222222").
  --track-color COLOR   Color of tracks (default: "#4DD2FF").
  --track-color2 COLOR  Secondary color of tracks (default: none).
  --text-color COLOR    Color of text (default: "#FFFFFF").
  --special-color COLOR
                        Special track color (default: "#FFFF00").
  --special-color2 COLOR
                        Secondary color of special tracks (default: none).
  --units UNITS         Distance units; "metric", "imperial" (default:
                        "metric").
  --clear-cache         Clear the track cache.
  --workers NUMBER_OF_WORKERS
                        Number of parallel track loading workers (default:
                        number of CPU cores)
  --from-strava FILE    JSON file containing config used to get activities
                        from strava
  --verbose             Verbose logging.
  --logfile FILE
  --special-distance DISTANCE
                        Special Distance1 by km and color with the
                        special_color
  --special-distance2 DISTANCE
                        Special Distance2 by km and color with the
                        special_color2
  --min-distance DISTANCE
                        min distance by km for track filter
  --activity-type ACTIVITY_TYPE, --activity ACTIVITY_TYPE
                        Filter tracks by activity type; e.g. 'running'
                        (default: all activity types)
  --with-animation      add animation to the poster
  --animation-time ANIMATION_TIME
                        animation duration (default: 30s)

Heatmap Type Options:
  --heatmap-center LAT,LNG
                        Center of the heatmap (default: automatic).
  --heatmap-radius RADIUS_KM
                        Scale the heatmap such that at least a circle with
                        radius=RADIUS_KM is visible (default: automatic).
  --heatmap-line-transparency-width TRANSP_1,WIDTH_1, TRANSP_2,WIDTH_2, TRANSP_3,WIDTH_3
                        Define three transparency and width tuples for the
                        heatmap lines or set it to `automatic` for automatic
                        calculation (default: 0.1,5.0, 0.2,2.0, 1.0,0.3).

Circular Type Options:
  --circular-rings      Draw distance rings.
  --circular-ring-color COLOR
                        Color of distance rings.
  --circular-ring-max-distance DISTANCE
                        Maximum distance for scaling the track lengths (in
                        given units).
```

Example:
```
create_poster --from-strava strava.json --type circular
create_poster --type grid --gpx-dir "my-tracks" --language "de" --year 2015 --title "Running" \
    --athlete "Florian Pigorsch" --special race1.gpx --special race2.gpx --special race3.gpx

create_poster --type github --gpx-dir "my-tracks" --language "de" --title "Running" \
    --athlete "Florian Pigorsch" --special-distance 10 --special-distance2 10 --special-color yellow --special-color2 red
```
creates a nice poster (`poster.svg`) of the GPX tracks in the directory `my-tracks` (see above).


### Selection of Tracks

`create_poster` tries to load all GPX files in the specified directory (option `--gpx-dir`).
To speed up subsequent executions of the script, successfully loaded GPX tracks are cached in an intermediate format that allows for fast loading; use the option `--clear-cache` to delete these files.
Tracks without time stamps and tracks recorded in the wrong year (option `--year`) are discarded.
Tracks shorter than 1km are discarded, too
If multiple tracks have been recorded within one hour, they are merged to a single track.

### Filtering activities `--from-strava FILE` by `activity_type`

When using `--from-strava FILE` option,
you may specify optional `activity_type` to filter only certain [type(s) of activity][strava-activity-type] to load.
Note, `activity_type` filters activities only when loading from strava, and will not affect what already cached.
That means if you change the value of `activity_type` you have to use `--clear-cache` to reload with the new filter.
You can provide `activity_type` with a list or a string.
All following examples are valid.

```json
{
    "client_id": "YOUR STRAVA API CLIENT ID",
    "client_secret": "YOUR STRAVA API CLIENT SECRET",
    "refresh_token": "YOUR STRAVA REFRESH TOKEN",
    "activity_type": "Run"
}
```

```json
{
    "client_id": "YOUR STRAVA API CLIENT ID",
    "client_secret": "YOUR STRAVA API CLIENT SECRET",
    "refresh_token": "YOUR STRAVA REFRESH TOKEN",
    "activity_type": ["Walk", "Hike"]
}
```

```json
{
    "client_id": "YOUR STRAVA API CLIENT ID",
    "client_secret": "YOUR STRAVA API CLIENT SECRET",
    "refresh_token": "YOUR STRAVA REFRESH TOKEN"
}
```

## Poster Types

Using the `--type` command line parameter, you can specify which type of poster to create:

### Grid Poster (`--type grid`)
The *Grid Poster* layouts all tracks in a grid, starting with the earliest track in the upper left corner of the poster, continuing with the second earliest track to the left, and so on.
*Special tracks* are drawn with the selected *special color*.
*Special distance tracks* are drawn with the selected *special color*.

![Example Grid Poster](https://raw.githubusercontent.com/flopp/GpxTrackPoster/main/examples/example_grid.png)
[svg](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_grid.svg)

### Calendar Poster (`--type calendar`)
The *Calendar Poster* draws one square for each day, each row of squares corresponds to specific month. If a track was recorded of a day the corresponding square is colored with the *track color* or with the *special color* if the track is marked as special. A day's total track length in kilometers is printed below each square.

![Example Calendar Poster](https://raw.githubusercontent.com/flopp/GpxTrackPoster/main/examples/example_calendar.png)
[svg](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_calendar.svg)

### Circular Poster (`--type circular`)
The *Circular Poster* the year in a circle; each day corresponds to a circle segment. The length of each segment corresponds to the total track distance of that day.

![Example Circular Poster](https://raw.githubusercontent.com/flopp/GpxTrackPoster/main/examples/example_circular.png)
[svg](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_circular.svg)

### Heatmap Poster (`--type heatmap`)
The *Heatmap Poster* displays all tracks within one "map". The more often a location has been "visited" on a track, the more colorful the corresponding location is on the map. *Special tracks* are drawn with the *special color*.

![Example Heatmap Poster](https://raw.githubusercontent.com/flopp/GpxTrackPoster/main/examples/example_heatmap.png)
[svg](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_heatmap.svg)

### Github Poster (`--type github`)
The *Github Poster* displays all tracks like github profile. *Special distance* are drawn with the *special color*.

![Example Github Poster](https://raw.githubusercontent.com/flopp/GpxTrackPoster/main/examples/example_github.png)
[svg](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_github.svg)



## Selection a Language
`create_poster` uses gettext to provide localization to other languages.
To select a different language than the default English, use the `--language LANGUAGE` option.
We currently support

- French (`--language fr_FR`)
- German (`--language de_DE`)
- Chinese (`--language zh_CN`)
- Russian (`--language ru_RU`)
- Finnish (`--language fi_FI`)

## Contributing
If you have found a bug or have a feature request, please create a new issue. I'm always happy improve the implementation!

Or even better: clone the repo, fix the bug/implement the feature yourself, and file a pull request. Contributions are always welcome!

Important: If you want to contribute via a pull request, make sure you run `make lint` and possibly `make format` and `make update-readme` before pushing code.

## Translation
The translation is based on GNUs 'gettext'.
For the translation of the month names to work, the language must be installed.

Use `locale -a` to check if the language is installed.

Use `locale-gen ru_RU.UTF-8` to install another language and update the locale `update-locale`.

### Add new translation
Example:
`msginit --input=gpxposter.pot --locale=de_DE --output=locale/de_DE/LC_MESSAGES/gpxposter.po`

### Update a translation
E.g. use [Poedit](https://poedit.net/) or [Localise Online Editor](https://localise.biz/free/poeditor) to edit the "po" files.  Afterwards compile that files.

### Create compiled translation file
`msgfmt gpxposter.po -o gpxposter.mo`

## License
[MIT](https://github.com/flopp/GpxTrackPoster/blob/master/LICENSE) &copy; 2016-2023 Florian Pigorsch

[strava-activity-type]: https://developers.strava.com/docs/reference/#api-models-ActivityType
