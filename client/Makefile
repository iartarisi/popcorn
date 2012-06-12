PREFIX?=.
CFLAGS=-g -Wall -fPIC
LDFLAGS=-L${PREFIX} -lpopcorn -lrpm
SO_TARGET=libpopcorn.so

all: popcorn

${SO_TARGET}:
	gcc ${CFLAGS} -shared -o libpopcorn.so libpopcorn.c

popcorn: ${SO_TARGET}


clean:
	rm -f *.o *.so popcorn /tmp/popcorn.txt