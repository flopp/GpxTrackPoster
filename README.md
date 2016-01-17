# GpxTrackPoster
Create a visually appealing poster from your GPX tracks - heavily inspired by https://www.madewithsisu.com/


## Usage
First of all, you need directory with a bunch of GPX files (e.g. you can export all your tracks from Garmin Connect with the excellent tool [garmin-connect-export](https://github.com/kjkjava/garmin-connect-export)).

You will need a little experience running things from the command line to use this script. That said, here are the usage details from the `--help` flag:

```
usage: create_poster.py [-h] [--gpx-dir DIR] [--output FILE] [--year YEAR]
               [--title TITLE] [--athlete NAME] [--special FILE] [--type TYPE]
               [--background-color COLOR] [--track-color COLOR]
               [--text-color COLOR] [--special-color COLOR] [--clear-cache]

optional arguments:
  -h, --help                show this help message and exit
  --gpx-dir DIR             Directory containing GPX files (default: current directory).
  --output FILE             Name of generated SVG image file (default: "poster.svg").
  --year YEAR               Filter tracks by year (default: past year)
  --title TITLE             Title to display (default: "My Tracks").
  --athlete NAME            Athlete name to display (default: "John Doe").
  --special FILE            Mark track file from the GPX directory as special; use multiple times to mark multiple tracks.
  --type TYPE               Type of poster to create (default: "grid", available: "calendar", "grid", "heatmap").
  --background-color COLOR  Background color of poster (default: "#222222").
  --track-color COLOR       Color of tracks (default: "#4DD2FF").
  --text-color COLOR        Color of text (default: "#FFFFFF").
  --special-color COLOR     Special track color (default: "#FFFF00").
  --clear-cache             Clear the track cache.
```

Example: `create_poster.py --type grid --gpx-dir "my-tracks" --year 2015 --title "Running" --athlete "Florian Pigorsch" --special race1.gpx --special race2.gpx --special race3.gpx` creates a nice poster (`poster.svg`) of the GPX tracks in the directory `my-tracks` (see above).


### Selection of Tracks

`create_poster.py` tries to load all GPX files in the specified directory (option `--gpx-dir`).
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

![Example Grid Poster](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_calendar.png)
[svg](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_calendar.svg)

### Heatmap Poster (`--type heatmap`)
The *Heatmap Poster* displays all tracks within one "map". The more often a location has been "visited" on a track, the more colorful the corresponding location is on the map. *Special tracks* are drawn with the *special color*.

![Example Grid Poster](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_heatmap.png)
[svg](https://github.com/flopp/GpxTrackPoster/blob/master/examples/example_heatmap.svg)

## Setup
1. Clone the repository: `git clone https://github.com/flopp/GpxTrackPoster.git`
2. `cd GpxTrackPoster`
3. Create virtualenv: `virtualenv -p /usr/bin/python3 venv`
4. Activate virtualenv: `source venv/bin/activate`
5. Install requirements: `pip install -r /path/to/requirements.txt`
6. Run `./create_poster.py` (see above)
7. Deactive virtualenv: `deactivate`


## License
[MIT](https://github.com/flopp/GpxTrackPoster/blob/master/LICENSE) &copy; 2016 florian Pigorsch
