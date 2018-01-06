lint:
	flake8 \
	    gpxtrackposter create_poster.py tests scripts

test:
	python -m pytest tests

update-readme:
	./create_poster.py --help | scripts/update_readme.py README.md
