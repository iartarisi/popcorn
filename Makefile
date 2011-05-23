FILES=README popcorn-client popcorn.conf popcorn.cron server/index.html server/popcorn-server server/server.conf

all: release

release: popcorn.tar.bz2

popcorn.tar.bz2: $(FILES)
	tar cf popcorn.tar $(FILES)
	bzip2 --best popcorn.tar
