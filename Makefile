lint:
	flake8 \
	    gpxtrackposter create_poster.py tests

test:
	python -m pytest tests
