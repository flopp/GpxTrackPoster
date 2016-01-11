# GpxTrackPoster
Create a visually appealing poster from your GPX tracks - heavily inspired by https://www.madewithsisu.com/

![Example Poster](https://github.com/flopp/GpxTrackPoster/blob/master/example.png)


## Usage
First of all, you need directory with a bunch of GPX files (e.g. you can export all your tracks from Garmin Connect with the excellent tool [garmin-connect-export](https://github.com/kjkjava/garmin-connect-export)).

You will need a little experience running things from the command line to use this script. That said, here are the usage details from the `--help` flag:

```
usage: create_poster.py [-h] [--gpx-dir DIR] [--year YEAR] [--title TITLE]
                        [--athlete NAME] [--background-color COLOR]
                        [--track-color COLOR] [--text-color COLOR]
                        [--highlight FILE] [--highlight-color COLOR]
                        [--output FILE] [--clear-cache]

optional arguments:
  -h, --help            show this help message and exit
  --gpx-dir DIR         Directory containing GPX files (default: current directory).
  --year YEAR           Filter tracks by year (default: past year)
  --title TITLE         Title to display (default: "My Tracks").
  --athlete NAME        Athlete name to display (default: "John Doe").
  --background-color COLOR
                        Background color of poster (default: "#222222").
  --track-color COLOR   Color of tracks (default: "#4DD2FF").
  --text-color COLOR    Color of text (default: "#FFFFFF").
  --highlight FILE      Highlight specified track file from the GPX directory; use multiple times to highlight multiple tracks.
  --highlight-color COLOR
                        Track highlighting color (default: "#FFFF00").
  --output FILE         Name of generated SVG image file (default: "poster.svg").
  --clear-cache         Clear the track cache.

```

Example: `create_poster.py --gpx-dir "my-tracks" --year 2015 --title "Running" --athlete "Florian Pigorsch" --highlight race1.gpx --highlight race2.gpx --highlight race3.gpx` creates a nice poster (`poster.svg`) of the GPX tracks in the directory `my-tracks` (see above).


### Selection of Tracks

`create_poster.py` tries to load all GPX files in the specified directory (option `--gpx-dir`).
To speed up subsequent executions of the script, successfully loaded GPX tracks are cached in an intermediate format that allows for fast loading; use the option `--clear-cache` to delete these files.
Tracks without time stamps and tracks recorded in the wrong year (option `--year`) are discarded.
Tracks shorter than 1km are discarded, too
If multiple tracks have been recorded within one hour, they are merged to a single track.

The tracks are then sorted by their respective start times and are printed in a grid in row first order.


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
