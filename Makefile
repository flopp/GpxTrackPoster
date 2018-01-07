lint: check-copyright flake8

test:
	@python -m pytest tests

flake8:
	@flake8 gpxtrackposter create_poster.py tests scripts

COPYRIGHT_FILES = README.md LICENSE create_poster.py gpxtrackposter/*.py tests/*.py scripts/*.py

check-copyright:
	@./scripts/check_copyright.py $(COPYRIGHT_FILES)

bump-year:
	@./scripts/bump_year.py $(COPYRIGHT_FILES)

update-readme:
	@./create_poster.py --help | ./scripts/update_readme.py README.md
