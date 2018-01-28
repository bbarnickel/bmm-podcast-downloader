# Idea

The contained python classes are just a rough implementation of

1) A minimal API to BMM which suffices the requirements of
2) a watcher class which is able to download the recent tracks
   of a given podcast id.

# BMM API - MinimalBmmApi class

Found in `bmmapi.py`. Requires to login via a BCC user's SSO credentials.
The API uses the python `requests` package.
See code for further details.

# Watcher - PodcastWatcher class

The watcher found in `watcher.py` is to be initialized with an already authenticated instance of `MinimalBmmApi`. Further it needs a path pointing to the directory where the downloaded tracks will be stored as well as the tracking database file.

The watcher keeps track of already downloaded tracks via a JSON encoded database in `database.json`. This should prevent unneccessary downloads.

The only public method `checkPodcastTracks` needs the podcast id and the languages which are to be checked. If a file is to be downloaded the given file name in the track's media url is used as the target file name. **IMPORTANT**: It is assumed that the given file names are unique! Otherwise files might be overwritten!

# Requirements

The API classs uses the *pip* package `requests`.

Best create a virtual environment and activate it:

~~~bash
$ pyvenv .venv
$ . .venv/bin/activate
~~~

In any case install the requirements:

~~~bash
$ pip -r requirements.txt
~~~

# Configuration

To use the watcher the program first needs to instantiate a `MinimalBmmApi` instance which needs the url to the BMM API. Further this instance needs to authenticate, which requires above mentioned credentials.

The watcher then only needs the target path.

See `download.py` for an example.
