/*
 * Copyright (c) 2012 Ionuț Arțăriși <mapleoin@lavabit.com>
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */

#include <stdio.h>

#include <rpm/rpmlib.h>
#include <rpm/rpmdb.h>
#include <rpm/rpmts.h>
#include <rpm/header.h>

void writePkgNVREA(Header header, FILE *output_f);
int popcornPostData(char *server_name, char *file_name);

int main(int argc, char **argv) {
    rpmReadConfigFiles(NULL, NULL);
    rpmts ts = rpmtsCreate();

    rpmdbMatchIterator iter = rpmtsInitIterator(ts, RPMTAG_NAME, NULL, 0);

    Header header;
    FILE *output_f = fopen("/tmp/popcorn.txt", "w");
    while ( (header = rpmdbNextIterator(iter) ) != NULL) {
        writePkgNVREA(header, output_f);
    }

    /* Cleanup*/
    fclose(output_f);
    rpmts rpmtsFree(rpmts ts);

    /* Upload data to the server */
    popcornPostData("http://popcorn.mapleoin.eu", "/tmp/popcorn.txt");

    return(0);
}
