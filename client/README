POPCORN - Popularity Contest (for RPM)
======================================

**MIT License**

Copyright (c) 2009-2011 Pavol Rusnak <stick@gk2.sk>

Copyright (c) 2011-2012 Ionuț Arțăriși <iartarisi@suse.cz>


Introduction
------------

Popcorn lists system packages and for each package it reads access time of its
"watched" files (see section Watched Files below). The most recent fileaccess
time is considered as the "package access time". The packages are then split into
four categories depending on the package install time and package access time:

* (r) recent
  - package has been recently installed (less than 30 days)
  - ( now - install_time < 30 days )
* (v) voted
  - package is older than 30 days and has been used in the last 30 days
  - ( now - install_time > 30 days ) and ( now - access_time < 30 days)
* (o) old
  - package is older than 30 days and hasn't been used recently
  - ( now - install_time > 30 days ) and ( now - access_time > 30 days)
* (n) nofiles
  - there are no watched files present in the package
  - access_time = 0

Each package falls exactly into one category, so (n + r + v + o) is the total
number of the installed packages.

Popcorn is inspired by Debian Popcon available from http://popcon.debian.org/


Packages
--------

popcorn-client

* client-side written in Python
* gathers info about packages and sends to server (via HTTP POST)

popcorn-server

* server which receives, processes, stores and displays submissions
* see README.server for more information


Submission format
-----------------

Format is plaintext. The first line contains the string POPCORN followed
by the popcorn version, distribution name and version, machine
architecture and uuid. Then the list of packages follows.

Each line represents one package, values are separated by space. First
value is one character describing the category (see Introduction),
second value is the package name, third, fourth and fifth are version,
release and epoch, sixth and seventh are architecture and repository of
the package.

Plaintext size is around 100 KiB on casual machine, which could be later
compressed to around 20 KiB using HTTP gzip compression.

Format:

```
POPCORN <popcorn-client_version> <distro_name> <distro_version> <arch> <hw_uuid>
<category> <package> <version> <release> <epoch> <arch> <repository>
...
<EOF>
```

Example:

```
POPCORN 0.1 openSUSE 12.1 i686 7f3a469b-c052-4c9a-aa97-bffdb55e9878
o libgmp3 4.3.2 1.13 None i586 openSUSE
o libfolks0 0.2.0 1.2 None i586 obs://build.opensuse.org/GNOME
v enchant 1.6.0 2.3 1 i586 openSUSE
o libx264-112 0.112svn20110115 1.pm.2.6 None i586 http://packman.links2linux.de
n myspell-british 20100316 16.1 None noarch Uknown
```

Watched files
-------------

To find out whether the package has been used recently, access times of the files
in the following directories are watched:

```
/bin
/boot
/lib
/lib64
/sbin
/usr/bin
/usr/games
/usr/include
/usr/lib
/usr/lib64
/usr/libexec
/usr/sbin
```

Note: if some of the filesystems are mounted with noatime, the packages
      from this filesystem are always in the category 'nofiles'


**Please check README.server.markdown for information on setting up the server**
