#!/bin/bash

for TYPE in grid calendar circular heatmap ; do
    ../create_poster.py --gpx-dir ../2016 --year 2016 \
        --athlete "Florian Pigorsch" --title "My Runs 2016" \
        --type $TYPE --output example_$TYPE.svg \
        --special 20161231-123107-Run.gpx \
        --special 20160916-171532-Run.gpx \
        --special 20160911-093006-Run.gpx \
        --special 20160710-075921-Run.gpx \
        --special 20160508-080955-Run.gpx \
        --special 20160403-091527-Run.gpx \
        --special 20160313-130016-Run.gpx \
        --special 20160117-101524-Run.gpx 
    
    # use headless inkscape to produce a png
    inkscape --without-gui --export-width 500 \
        --file example_$TYPE.svg --export-png example_$TYPE.png
done
