.PHONY: check-copyright bump-year update-readme format extract-messages


COPYRIGHT_FILES = README.md LICENSE gpxtrackposter/*.py tests/*.py scripts/*.py

check-copyright:
	@./scripts/check_copyright.py $(COPYRIGHT_FILES)

bump-year:
	@./scripts/bump_year.py $(COPYRIGHT_FILES)

update-readme:
	@./gpxtrackposter/cli.py --help | ./scripts/update_readme.py README.md

format:
	@black gpxtrackposter/*.py tests/*.py scripts/*.py

extract-messages:
	xgettext --keyword="trans" -d gpxposter -o locale/gpxposter.pot gpxtrackposter/*.py
	msgmerge --update locale/de_DE/LC_MESSAGES/gpxposter.po locale/gpxposter.pot
	msgmerge --update locale/fi_FI/LC_MESSAGES/gpxposter.po locale/gpxposter.pot
	msgmerge --update locale/fr_FR/LC_MESSAGES/gpxposter.po locale/gpxposter.pot
	msgmerge --update locale/ru_RU/LC_MESSAGES/gpxposter.po locale/gpxposter.pot
	msgmerge --update locale/zh_CN/LC_MESSAGES/gpxposter.po locale/gpxposter.pot

compile-messages:
	msgfmt -o locale/de_DE/LC_MESSAGES/gpxposter.mo locale/de_DE/LC_MESSAGES/gpxposter
	msgfmt -o locale/fi_FI/LC_MESSAGES/gpxposter.mo locale/fi_FI/LC_MESSAGES/gpxposter
	msgfmt -o locale/fr_FR/LC_MESSAGES/gpxposter.mo locale/fr_FR/LC_MESSAGES/gpxposter
	msgfmt -o locale/ru_RU/LC_MESSAGES/gpxposter.mo locale/ru_RU/LC_MESSAGES/gpxposter
	msgfmt -o locale/zh_CN/LC_MESSAGES/gpxposter.mo locale/zh_CN/LC_MESSAGES/gpxposter

