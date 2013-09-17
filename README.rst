sc
==

``sc`` is a command-line interface for Soundcloud. It allows you to
compress and upload audio to Soundcloud, among other things.

Install
-------

Preferred method of install is ``pip``:

::

    $ pip install sc-cli

After installing ``sc``, you should authenticate using ``sc auth``.

Commands
--------

Check usage for detailed arguments:

::

    $ sc --help

auth
~~~~

Authenticate against Soundcloud and save access\_token. Required to
upload audio.

::

    $ sc auth
    Enter username (zk): requite
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

share
~~~~~

Share a track with a set of users on Soundcloud.

::

    $ sc share https://soundcloud.com/requite/honey/s-nIqsG zeekay
    shared with:
      zeekay (http://soundcloud.com/zeekay)

upload
~~~~~~

You can use the ``sc upload`` command to upload audio to Soundcloud. If
you specify a ``.wav`` file ``sc`` will compress the audio for you (if
``lame`` is installed). By default uploaded audio is set to private, and
you'll get the secret link for sharing:

::

    $ sc honey.wav
    uploading honey.mp3 [==================================================] 100%
    http://soundcloud.com/requite/honey/s-nIqsG

API
---

sc.lame.compress(filename, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compress track with lame. Callback if specified while be fed a line to
use to display progress.

sc.api.client.get\_access\_token(username, password)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Authenticate against Soundcloud and return access token.

sc.api.client.get\_client(access\_token=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Return soundcloud client using specified or saved access\_token.

sc.api.share.share(track\_id=None, url=None, users=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Share a track with given users.

sc.api.upload.upload(filename, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Upload track to soundcloud.
