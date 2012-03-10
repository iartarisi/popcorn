Server setup
------------

The server is using in Python, using the Flask web framework and SQLAlchemy for the models.

To install the server in a virtualenv do the following:

Clone the repository

```git clone git://github.com/mapleoin/popcorn.git
```  

Create the virtualenv and activate it

```
$ virtualenv vpopcorn
$ source vpopcorn/bin/activate
```

You will need the postgresql development files to install psycopg2 which
is a required dependency for popcorn you should install this using your
distribution's package manager. Example: `zypper install gcc postgresql-devel`

Set up your development environment. This will add the popcorn package
to your python path, but will not install it anywhere else. You can now
edit the files in the git clone directory and the changes will be
immediately visible to the server.

```
$ cd popcorn
$ ./setup.py develop
```

You can check that the unittests run fine

```$ ./setup.py test```

Install and setup postgresql-server for your distribution, then turn it
on. Create the popcorn user and database.

```
$ su - postgres
$ createuser popcorn -P
Enter password for new role: <enter popcorn as the password>
Enter it again: <popcorn again>
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) n
Shall the new role be allowed to create more new roles? (y/n) n
$ createdb popcorn --owner=popcorn
```

If you've set different values here than the default, edit `DB_ENGINE` in
 `popcorn/configs.py` and set them there as well

Initialize the database (installs tables and initial data).

```$ ./server/popcorn-server init_db
```

Start the server with the `--debug` flag (changes to files will cause
the server to reload them immediately + nice traceback pages)

```
$ ./server/popcorn-server --debug
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
```
 
You can now point your browser to http://127.0.0.1:5000/ (there won't be
 much to see).


Client
------
 
In order to test the client, you will need to have the `python-rpm`
package installed. It's easier to do this from outside the virtualenv,
because virtualenv will hide your system's site-packages by default (and
this is also how `popcorn-client` will run *in the wild*).

```
$ POPCORN_ENABLED=1 ./popcorn-client 
Submission received. Thanks!
```

If you now look on the popcorn webUI, you should see a lot of data about
your currently installed packages.