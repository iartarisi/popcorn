FILES=README popcorn-client popcorn.conf popcorn.cron setup.py MANIFEST.in
DIRS=popcorn server

all: release

release: popcorn.tar.bz2

popcorn.tar.bz2: $(FILES) $(DIRS)
	tar cf popcorn.tar $(FILES) $(DIRS)
	bzip2 --best popcorn.tar

clean:
	rm -rf popcorn.tar.bz2

test:
	python -m unittest discover

coverage:
	coverage run --source=popcorn /usr/bin/unit2 discover
	coverage report -m
	rm .coverage


