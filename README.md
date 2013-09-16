# sc
`sc` is a command-line interface (and library for) interacting with Soundcloud.
It will eventually support several features, but as of right now you can
compress & upload audio to soundcloud.

## Install
Preferred method of install is `pip`:

    $ pip install sc-cli

Then run `sc auth` to authenticate with Soundcloud: `sc` will try to guess your
username based on your system account name:

    $ sc auth
    Enter username (zk): requite
    Enter password:
    Saved access_token.

## Usage
You can use the `sc upload` command to upload audio to Soundcloud. If you
specify a `.wav` file `sc` will compress the audio for you (if `lame` is
installed). By default uploaded audio is set to private, and you'll get the secret
link for sharing:

    $ sc upload mysong.mp3
    uploading mysong.mp3 [==================================================] 100%
    http://soundcloud.com/requite/mysong/s-oFATH

You can also specify tons of other options, genre, tags etc. Check the usage
with `--help`:

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
