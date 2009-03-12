CC = gcc
CFLAGS = -Wall
LDFLAGS = -ltdb

all: popcorn-server

popcorn-server: popcorn-server.o
	$(CC) $(LDFLAGS) $< -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f *.o popcorn-server
