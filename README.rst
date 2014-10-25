soundcloud-cli
==============

``soundcloud-cli`` is a command-line interface for
`SoundCloud <http://soundcloud.com>`__. It allows you to compress and
upload audio to SoundCloud, among other things.

Install
-------

Preferred method of install is ``pip``:

::

    $ pip install soundcloud-cli

After installing ``sc``, you should authenticate using ``sc auth``.

Commands
--------

Check usage for detailed arguments:

::

    $ sc --help

auth
~~~~

Authenticate against SoundCloud and save access\_token. Required to
upload audio.

::

    $ sc auth
    Enter username (zeekay): requite
    Enter password:
    Saved access_token.

You can run ``sc auth`` to change users later.

defaults
~~~~~~~~

Set values to be used as defaults for commands.

::

    $ sc defaults share_with zeekay
    set share_with = ['zeekay']

list
~~~~

List your tracks, or tracks for a given user.

::

    $ sc list sinerise
    tracks by sinerise:
      Dane Pedersen - Space Jambience (Sinerise Remix)   http://soundcloud.com/sinerise/space-jambience-remix
      Strewn (51st Vocal Mix) feat. delica               http://soundcloud.com/sinerise/strewn-51st-vocal-mix
      Calling (requite's bass refix)                     http://soundcloud.com/sinerise/calling-refix
      Can't Save Me                                      http://soundcloud.com/sinerise/cant-save-me
      Strewn                                             http://soundcloud.com/sinerise/strewn
      Calling (Original)                                 http://soundcloud.com/sinerise/calling

share
~~~~~

Share a track with a set of users on SoundCloud.

::

    $ sc share https://soundcloud.com/requite/honey/s-nIqsG zeekay
    shared with:
      zeekay (http://soundcloud.com/zeekay)

upload
~~~~~~

You can use the ``sc upload`` command to upload audio to SoundCloud. If
you specify a ``.wav`` file ``sc`` will compress the audio for you (if
``lame`` is installed). By default uploaded audio is set to private, and
you'll get the secret link for sharing:

::

    $ sc honey.wav
    uploading honey.mp3 [==================================================] 100%
    http://soundcloud.com/requite/honey/s-nIqsG

