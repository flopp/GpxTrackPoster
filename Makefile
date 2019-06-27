.PHONY: check-copyright bump-year update-readme format


COPYRIGHT_FILES = README.md LICENSE gpxtrackposter/*.py tests/*.py scripts/*.py

check-copyright:
	@./scripts/check_copyright.py $(COPYRIGHT_FILES)

bump-year:
	@./scripts/bump_year.py $(COPYRIGHT_FILES)

update-readme:
	@./gpxtrackposter/cli.py --help | ./scripts/update_readme.py README.md

format:
	@black gpxtrackposter/*.py tests/*.py scripts/*.py
