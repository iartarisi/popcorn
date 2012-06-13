PREFIX?=.
CFLAGS=-g -Wall -fPIC
LDFLAGS=-L${PREFIX} -lpopcorn -lrpm -lcurl
SO_TARGET=libpopcorn.so

all: popcorn

${SO_TARGET}:
	gcc ${CFLAGS} -lrpm -shared -o libpopcorn.so libpopcorn.c

popcorn: ${SO_TARGET}


clean:
	rm -f *.o *.so popcorn /tmp/popcorn.txt
