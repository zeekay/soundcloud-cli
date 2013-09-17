# sc
`sc` is a command-line interface for Soundcloud. It allows you to compress and
upload audio to Soundcloud, and will eventually support many other useful
features.

## Install
Preferred method of install is `pip`:

    $ pip install sc-cli

After installing `sc`, you should authenticate with Soundcloud.

    $ sc auth
    Enter username (zk): requite
    Enter password:
    Saved access_token.

You can run `sc auth` to change users later.


## Commands
Check usage for detailed arguments:

    $ sc --help

### auth
Authenticate against Soundcloud and save access_token. Can be run multiple times
to switch between users

### defaults
Set values to be used as defaults for commands.

### share
Share a track with a set of users on Soundcloud.

### upload
You can use the `sc upload` command to upload audio to Soundcloud. If you
specify a `.wav` file `sc` will compress the audio for you (if `lame` is
installed). By default uploaded audio is set to private, and you'll get the secret
link for sharing:

    $ sc upload mysong.mp3
    uploading mysong.mp3 [==================================================] 100%
    http://soundcloud.com/requite/mysong/s-oFATH

## API

### sc.lame.compress(filename, **kwargs)
Compress track with lame. Callback if specified while be fed a line to use to
display progress.

### sc.api.client.get_access_token(username, password)
Authenticate against Soundcloud and return access token.

### sc.api.client.get_client(access_token=None)
Return soundcloud client using specified or saved access_token.

### sc.api.share.share(track_id=None, url=None, users=None)
Share a track with given users.

### sc.api.upload.upload(filename, **kwargs)
Upload track to soundcloud.
