sc
==

``sc`` is a command-line interface for Soundcloud. It allows you to
compress and upload audio to Soundcloud, and will eventually support
many other useful features.

Install
-------

Preferred method of install is ``pip``:

::

    $ pip install sc-cli

After installing ``sc``, you should authenticate with Soundcloud.

::

    $ sc auth
    Enter username (zk): requite
    Enter password:
    Saved access_token.

You can run ``sc auth`` to change users later.

Usage
-----

You can use the ``sc upload`` command to upload audio to Soundcloud. If
you specify a ``.wav`` file ``sc`` will compress the audio for you (if
``lame`` is installed). By default uploaded audio is set to private, and
you'll get the secret link for sharing:

::

    $ sc upload mysong.mp3
    uploading mysong.mp3 [==================================================] 100%
    http://soundcloud.com/requite/mysong/s-oFATH

You can also specify tons of other options, genre, tags etc. Check the
usage with ``--help``:

::

    $ sc upload --help
    usage: sc upload [-h] [--public] [--compress] [--no-compress] [--downloadable]
                     [--no-downloadable] [--bitrate BITRATE] [--artist ARTIST]
                     [--title TITLE] [--album ALBUM] [--year YEAR]
                     [--description DESCRIPTION] [--genre GENRE] [--tags TAGS]
                     [--artwork ARTWORK]
                     filename

    positional arguments:
      filename              filename to upload

    optional arguments:
      -h, --help            show this help message and exit
      --public              make track public
      --compress            compress file
      --no-compress         do not compress file
      --downloadable        allow downloads
      --no-downloadable     disallow downloads
      --bitrate BITRATE     bitrate for compression
      --artist ARTIST       id3 title
      --title TITLE         id3 title
      --album ALBUM         id3 album
      --year YEAR           id3 year
      --description DESCRIPTION
                            description of track
      --genre GENRE         genre of track
      --tags TAGS           comma separated list of tags
      --artwork ARTWORK     artwork to use for song

