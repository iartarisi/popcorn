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

#define MAX_DATA 100 /* upper limit when reading from files */

/* Return the popcorn status of a package, by looking at the status of
 * the files contained in the rpm. The return status is a char. which
 * can be: v (voted), o (old), n (nofiles), r (recent) */
char getPkgStatus(Header header, const char* pkg_name) {
    return 'v';
}

/* Get a header string value */
const char* headerGetS(Header header, int rpmTag,
                       const char *defvalue) {
    static int type;
    static int count;
    static const char *value;
    if (!(headerGetEntry(header, rpmTag, &type, (void **) &value, &count)
          && type == RPM_STRING_TYPE && count == 1))
        value = defvalue;
    return value;
}
    
/* Write a line of information corresponding to the package whose header
 * has been passed in as the first argument to the file passed as the
 * second argument. */
void writePkgLine(Header header, FILE *output_f) {
    static const char *name;
    static const char *version;
    static const char *release;
    static const char *arch;
    static const char *epoch;
    static const char *vendor;

    headerNEVRA(header, &name, NULL, &version, &release, &arch);

    /* skip any gpg-pubkey packages */
    if (!strcmp(name, "gpg-pubkey"))
        return ;
        
    /* headerNEVRA doesn't return the epoch, so we have to get it manually */
    epoch = headerGetS(header, RPMTAG_EPOCH, "None");

    vendor = headerGetS(header, RPMTAG_VENDOR, "Unknown");
    
    static char status;
    status = getPkgStatus(header, name);

    fprintf(output_f, "%c %s %s %s %s %s %s\n",
            status, name, version, release, epoch, arch, vendor);
}

/* Read the system ID from a file and return it */
char *getSystemID() {
    FILE *hwuuid_file;
    char buf[1024];
    char *system_id;
    /* Open file and read the ID */
    hwuuid_file = fopen("/etc/smolt/hwuuid", "r");
    if (!hwuuid_file)
        return NULL;
    system_id = fgets(buf, 37, hwuuid_file);
    /* Cleanup */
    fclose(hwuuid_file);
    return system_id;
}

/* Determine the OS name and return it */
char *getOSName() {
    return "SLES";
}

/* Determine the OS version and return it */
char *getOSVersion() {
    return "11SP1";
}

/* Determine the OS arch and write it to the 'arch' parameter */
void getOSArch(char *arch) {
    FILE *parch;

    /* Use the 'arch' system utility to get the system's arch */
    parch = popen("arch", "r");
    if (parch == NULL) {
        printf("Failed to read system architecture.\n");
        exit(1);
    }

    int rc = fscanf(parch, "%s", arch);
    if (rc != 1) {
        printf("Failed to read system architecture.\n");
        exit(rc);
    }
    pclose(parch);
}

/* Write the heading to a given file handle */
void writeHeading(FILE *output_f) {
    char arch[MAX_DATA];

    getOSArch(arch);
    fprintf(output_f, "POPCORN 0.1 %s %s %s %s\n",
            getOSName(), getOSVersion(), arch, getSystemID());
}

/* Post data from a file given by the second argument to a server given by the
 * first argument */
long popcornPostData(char *server_name, char *file_name) {
    CURL *curl;
    CURLcode curl_code;
    long http_code = 0;

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
