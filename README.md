# GpxTrackPoster
Create a visually appealing poster from your GPX tracks.

## Usage
First of all, you need directory with a bunch of GPX files (e.g. you can export all your tracks from Garmin Connect with the excellent tool [garmin-connect-export](https://github.com/kjkjava/garmin-connect-export)).

You will need a little experience running things from the command line to use this script. That said, here are the usage details from the `--help` flag:

```
usage: create_poster.py [-h] [--gpx-dir DIR] [--year YEAR] [--title TITLE]
                        [--athlete NAME] [--background-color COLOR]
                        [--track-color COLOR] [--text-color COLOR]
                        [--output FILE]

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
  --output FILE         Name of generated SVG image file (default: "poster.svg").
```

Example: `create_poster.py --gpx-dir "my-tracks" --year 2015 --title "Running" --athlete "Florian Pigorsch"` creates a nice poster (`poster.svg`) of the GPX tracks in the directory `my-tracks`:



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
