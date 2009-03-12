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
#include <string.h>
#include <fcntl.h>
#include <signal.h>
#include <tdb.h>

#define STATSDIR  "/var/cache/popcorn/"
#define STATSFILE "stats.tdb"

#define SILENT 0

#define BUFSIZE 1024

#define is_sane(c) ( ((c)>='A'&&(c)<='Z') || ((c)>='a'&&(c)<='z') || ((c)>='0'&&(c)<='9') || ((c)=='.') || ((c)=='-') || ((c)=='_') )

typedef struct {
    unsigned int n; /* no-files */
    unsigned int r; /* recent */
    unsigned int v; /* voted */
    unsigned int o; /* old */
} TUPLE;

void sanitize(char *str)
{
    char *c = str;
    while (*c)
    {
        if (!is_sane(*c))
        {
            str[0]='\0'; break;
        }
        ++c;
    }
    if (str[0]=='\0') strcpy(str,"unknown");
}

int main()
{
    int l;
    unsigned int cnt;
    char buf[BUFSIZE], ver[BUFSIZE], arch[BUFSIZE], cat, *pkg, *c;
    TDB_CONTEXT *db;
    TDB_DATA key, val;
    TUPLE tuple;

    /* read from stdin until line starting with "POPCORN " comes */
    while (fgets(buf, BUFSIZE, stdin)) {
        if (!strncmp(buf, "POPCORN ", 8)) break;
    }
    /* if not present then exit */
    if (strncmp(buf, "POPCORN ", 8)) {
#if !SILENT
        fprintf(stderr, "Popcorn header not found\n");
#endif
        return 1;
    }
    /* read and sanitize version and architecture */
    sscanf(buf, "POPCORN %s %s", ver, arch);
    sanitize(ver);
    sanitize(arch);

    /* open database */
    db = tdb_open(STATSDIR STATSFILE, 0, 0, O_CREAT | O_RDWR, 0644);
    if ( !db ) {
#if !SILENT
        fprintf(stderr, "Can't open database: %s\n", STATSDIR STATSFILE);
#endif
        return 1;
    }

    // update architecture field
    key.dsize = strlen(arch) + 5;
    sprintf(buf, "arch/%s", arch);
    key.dptr = (unsigned char *)buf;
    val = tdb_fetch(db, key);
    cnt = val.dptr ? *((unsigned int *)val.dptr) + 1 : 1;
    val.dptr = (unsigned char *)&cnt;
    val.dsize = sizeof(cnt);
    tdb_store(db, key, val, TDB_REPLACE);

    // update version field
    key.dsize = strlen(ver) + 4;
    sprintf(buf, "ver/%s", ver);
    key.dptr = (unsigned char *)buf;
    val = tdb_fetch(db, key);
    cnt = val.dptr ? *((unsigned int *)val.dptr) + 1 : 1;
    val.dptr = (unsigned char *)&cnt;
    val.dsize = sizeof(cnt);
    tdb_store(db, key, val, TDB_REPLACE);

    // update packages
    while (fgets(buf, BUFSIZE, stdin)) {
        l = strlen(buf);
        if (l<3) continue;
        cat = buf[0];
        c = strpbrk(buf + 2, " \n\r\t");
        *c = '\0';
        pkg = buf + 2;

        key.dsize = strlen(pkg);
        key.dptr = (unsigned char *)pkg;
        val = tdb_fetch(db, key);
        if (!val.dptr) {
            tuple.n = 0;
            tuple.r = 0;
            tuple.v = 0;
            tuple.o = 0;
        } else {
            tuple = *((TUPLE *)val.dptr);
        }
        switch (cat) {
            case 'n': ++tuple.n; break;
            case 'r': ++tuple.r; break;
            case 'v': ++tuple.v; break;
            case 'o': ++tuple.o; break;
        }
        val.dptr = (unsigned char *)&tuple;
        val.dsize = sizeof(tuple);
        tdb_store(db, key, val, TDB_REPLACE);
    }

    tdb_close(db);
    return 0;
}
