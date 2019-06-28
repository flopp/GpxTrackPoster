[![Build Status](https://travis-ci.org/flopp/GpxTrackPoster.svg?branch=master)](https://travis-ci.org/flopp/GpxTrackPoster)
![License MIT](https://img.shields.io/badge/license-MIT-lightgrey.svg?style=flat)

# GpxTrackPoster
Create a visually appealing poster from your GPX tracks - heavily inspired by https://www.instagram.com/p/Behppx9HCfx/


## Usage
First of all, you need directory with a bunch of GPX files (e.g. you can export all your tracks from Garmin Connect with the excellent tool [garmin-connect-export](https://github.com/kjkjava/garmin-connect-export), or use [StravaExportToGPX](https://github.com/flopp/StravaExportToGPX) to convert the activities in a Strava export zip file to GPX).

You will need a little experience running things from the command line to use this script. That said, here are the usage details from the `--help` flag:

```
usage: create_poster [-h] [--gpx-dir DIR] [--output FILE]
                     [--language LANGUAGE] [--year YEAR] [--title TITLE]
                     [--athlete NAME] [--special FILE] [--type TYPE]
                     [--background-color COLOR] [--track-color COLOR]
                     [--track-color2 COLOR] [--text-color COLOR]
                     [--special-color COLOR] [--special-color2 COLOR]
                     [--units UNITS] [--clear-cache] [--verbose]
                     [--logfile FILE] [--heatmap-center LAT,LNG]
                     [--heatmap-radius RADIUS_KM] [--circular-rings]
                     [--circular-ring-color COLOR]

optional arguments:
  -h, --help            show this help message and exit
  --gpx-dir DIR         Directory containing GPX files (default: current
                        directory).
  --output FILE         Name of generated SVG image file (default:
                        "poster.svg").
  --language LANGUAGE   Language (default: english).
  --year YEAR           Filter tracks by year; "NUM", "NUM-NUM", "all"
                        (default: all years)
  --title TITLE         Title to display (default: "My Tracks").
  --athlete NAME        Athlete name to display (default: "John Doe").
  --special FILE        Mark track file from the GPX directory as special; use
                        multiple times to mark multiple tracks.
  --type TYPE           Type of poster to create (default: "grid", available:
                        "grid", "calendar", "heatmap", "circular").
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
  --verbose             Verbose logging.
  --logfile FILE

Heatmap Type Options:
  --heatmap-center LAT,LNG
                        Center of the heatmap (default: automatic).
  --heatmap-radius RADIUS_KM
                        Scale the heatmap such that at least a circle with
                        radius=RADIUS_KM is visible (default: automatic).

Circular Type Options:
  --circular-rings      Draw distance rings.
  --circular-ring-color COLOR
                        Color of distance rings.
```

Example:
```
create_poster --type grid --gpx-dir "my-tracks" --language "de" --year 2015 --title "Running" \
    --athlete "Florian Pigorsch" --special race1.gpx --special race2.gpx --special race3.gpx
```
creates a nice poster (`poster.svg`) of the GPX tracks in the directory `my-tracks` (see above).


### Selection of Tracks

`create_poster` tries to load all GPX files in the specified directory (option `--gpx-dir`).
To speed up subsequent executions of the script, successfully loaded GPX tracks are cached in an intermediate format that allows for fast loading; use the option `--clear-cache` to delete these files.
Tracks without time stamps and tracks recorded in the wrong year (option `--year`) are discarded.
Tracks shorter than 1km are discarded, too
If multiple tracks have been recorded within one hour, they are merged to a single track.

## Poster Types

Using the `--type` command line parameter, you can specify which type of poster to create:

### Grid Poster (`--type grid`)
The *Grid Poster* layouts all tracks in a grid, starting with the earliest track in the upper left corner of the poster, continuing with the second earliest track to the left, and so on.
*Special tracks* are drawn with the selected *special color*.

![Example Grid Poster](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_grid.png)
[svg](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_grid.svg)

### Calendar Poster (`--type calendar`)
The *Calendar Poster* draws one square for each day, each row of squares corresponds to specific month. If a track was recorded of a day the corresponding square is colored with the *track color* or with the *special color* if the track is marked as special. A day's total track length in kilometers is printed below each square.

![Example Calendar Poster](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_calendar.png)
[svg](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_calendar.svg)

### Circular Poster (`--type circular`)
The *Circular Poster* the year in a circle; each day corresponds to a circle segment. The length of each segment corresponds to the total track distance of that day.

![Example Circular Poster](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_circular.png)
[svg](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_circular.svg)

### Heatmap Poster (`--type heatmap`)
The *Heatmap Poster* displays all tracks within one "map". The more often a location has been "visited" on a track, the more colorful the corresponding location is on the map. *Special tracks* are drawn with the *special color*.

![Example Heatmap Poster](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_heatmap.png)
[svg](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_heatmap.svg)


## Selection a Language
`create_poster` uses gettext to provide localization to other languages.
To select a different language than the default English, use the `--language LANGUAGE` option.
We currently support

- French (`--language fr_FR`)
- German (`--language de_DE`)


## Setup
1. Clone the repository: `git clone https://github.com/flopp/GpxTrackPoster.git`
2. `cd GpxTrackPoster`
3. Create virtualenv: `virtualenv -p /usr/bin/python3 venv`
4. Activate virtualenv: `source venv/bin/activate`
5. Install the package: `pip install .`
6. Install development requirements (only if you want to contribute code!): `pip install -r requirements-dev.txt`
7. Run `create_poster` (see above)
8. Deactivate virtualenv: `deactivate`

## Contributing
If you have found a bug or have a feature request, please create a new issue. I'm always happy improve the implementation!

Or even better: clone the repo, fix the bug/implement the feature yourself, and file a pull request. Contributions are always welcome!

Important: If you want to contribute via a pull request, make sure you run `tox` and possibly `make format` before pushing code.

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
[MIT](https://github.com/flopp/GpxTrackPoster/blob/master/LICENSE) &copy; 2016-2019 Florian Pigorsch
