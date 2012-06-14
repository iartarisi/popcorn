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
#include <string.h>

#include <rpm/rpmlib.h>
#include <rpm/header.h>
#include <curl/curl.h>


void writePkgNVREA(Header header, FILE *output_f) {
    static const char *name;
    static const char *version;
    static const char *release;
    static const char *arch;
    static const char *epoch;

    headerNEVRA(header, &name, NULL, &version, &release, &arch);

    /* skip any gpg-pubkey packages */
    if (!strcmp(name, "gpg-pubkey"))
        return ;
        
    /* headerNEVRA doesn't return the epoch,
       so we have to get it manually */
    int type;
    int count;
    if (!(headerGetEntry(header, RPMTAG_EPOCH, &type, (void **) epoch, &count)
          && type == RPM_STRING_TYPE && count == 1))
        epoch = NULL;

    if (epoch != NULL)
        fprintf(output_f, "%s-%s-%s-%s.%s\n", name, epoch, version, release, arch);
    else
        fprintf(output_f, "%s-%s-%s.%s\n", name, version, release, arch);
}

/** Post data from a file to a given server */
int popcornPostData(char *server_name, char *file_name) {
    CURL *curl;
    CURLcode curl_code;
    int http_code = 0;

    struct curl_httppost *formpost = NULL;
    struct curl_httppost *lastptr = NULL;
    struct curl_slist *headerlist = NULL;
    static const char buf[] = "Expect:";

    curl_global_init(CURL_GLOBAL_ALL);

    /* Add file content to the request */
    curl_formadd(&formpost,
                 &lastptr,
                 CURLFORM_COPYNAME, "popcorn",
                 CURLFORM_FILE, file_name,
                 CURLFORM_END);

    /* Initialize */
    curl = curl_easy_init();
    headerlist = curl_slist_append(headerlist, buf);
    if (curl) {
        /* Set options */
        curl_easy_setopt(curl, CURLOPT_URL, server_name);
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headerlist);
        curl_easy_setopt(curl, CURLOPT_HTTPPOST, formpost);
        /* Set to 1 to suppress output in case of errors */
        curl_easy_setopt(curl, CURLOPT_FAILONERROR, 0);

        /* Perform the request */
        curl_code = curl_easy_perform(curl);

        /* Get the HTTP return code */
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);

        /* Cleanup */
        curl_easy_cleanup(curl);
        curl_formfree(formpost);
        curl_slist_free_all(headerlist);
    }
    return http_code;
}
