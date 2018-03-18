lint: check-copyright flake8 spell

test:
	@python -m compileall create_poster.py gpxtrackposter
	@python -m pytest tests

flake8:
	@flake8 gpxtrackposter create_poster.py tests scripts

spell:
	@codespell gpxtrackposter/*.py create_poster.py tests/*.py scripts/*.py

COPYRIGHT_FILES = README.md LICENSE create_poster.py gpxtrackposter/*.py tests/*.py scripts/*.py

check-copyright:
	@./scripts/check_copyright.py $(COPYRIGHT_FILES)

bump-year:
	@./scripts/bump_year.py $(COPYRIGHT_FILES)

update-readme:
	@./create_poster.py --help | ./scripts/update_readme.py README.md
