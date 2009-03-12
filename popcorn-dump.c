/*
  Copyright (c) 2009 Pavol Rusnak <stick@gk2.sk>

  Permission is hereby granted, free of charge, to any person
  obtaining a copy of this software and associated documentation
  files (the "Software"), to deal in the Software without
  restriction, including without limitation the rights to use,
  copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the
  Software is furnished to do so, subject to the following
  conditions:

  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
  OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
  OTHER DEALINGS IN THE SOFTWARE.
*/

#include <stdio.h>
#include <fcntl.h>
#include <signal.h>
#include <unistd.h>
#include <tdb.h>

#define STATSDIR  "/var/cache/popcorn/"
#define STATSFILE "stats.tdb"

int cb(TDB_CONTEXT *db, TDB_DATA key, TDB_DATA val, void *dummy)
{
    int i, *vals;
    printf("%.*s", (int)key.dsize, key.dptr);
    vals = (int *)val.dptr;
    for (i=0; i<val.dsize/sizeof(int); i++)
        printf(" %d", vals[i]);
    printf("\n");
    return 0;
}

int main()
{
    TDB_CONTEXT *db;

    db = tdb_open(STATSDIR STATSFILE, 0, 0, O_RDONLY, 0644);

    tdb_traverse(db, cb, NULL);

    tdb_close(db);

    return 0;
}
