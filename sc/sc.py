import json
import os
import sys
from datetime import date

import soundcloud
from __init__ import __version__
from upload import upload

CLIENT_ID     = 'ffc80dc8b5bd435a15f9808724f73c40'
CLIENT_SECRET = 'b299b6681e00dfd9f5015639c7f5fe29'
SC_CONF       = os.path.expanduser('~/.sc')
DEFAULT_YEAR  = date.today().year


def get_access_token(username, password):
    client = soundcloud.Client(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        username=username,
        password=password,
        scope='non-expiring',
    )

    return client.access_token


def get_settings():
    if get_settings._cache:
        return get_settings._cache

    if not os.path.exists(SC_CONF):
        print 'Run auth command to authenticate and save access token.'
        sys.exit(1)

    with open(SC_CONF) as f:
        get_settings._cache = settings = json.load(f)

    return settings
get_settings._cache = None


def get_client(access_token=None):
    if not access_token:
        access_token = get_settings()['access_token']

    return soundcloud.Client(access_token=access_token)


def compress_track(filename, artist=None, title='', album='', year=DEFAULT_YEAR, bitrate=320):
    if not artist:
        artist = get_settings()['username']

    os.system('lame -b %d --tt "%s" --ta "%s" --tl "%s" --ty %s "%s"' % (bitrate, title, artist, album, year, filename))


def command_upload(args):
    access_token = get_settings()['access_token']

    if args.compress and args.filename.endswith('.wav'):
        print 'compressing file...'
        compress_track(args.filename, bitrate=args.bitrate,
                                      title=args.title,
                                      artist=args.artist,
                                      album=args.album,
                                      year=args.year)

        args.filename = args.filename.replace('.wav', '.mp3')

    if args.public:
        sharing = 'public'
    else:
        sharing = 'private'

    if args.tags:
        tag_list = [x.strip() for x in args.tags.split(',')]
    else:
        tag_list = []

    res = upload(args.filename, access_token, sharing=sharing,
                                              downloadable=args.downloadable,
                                              title=args.title,
                                              description=args.description,
                                              genre=args.genre,
                                              tag_list=tag_list,
                                              artwork=args.artwork)

    print res['permalink_url']


def command_auth(args):
    import getpass

    _username = getpass.getuser()
    username = raw_input('Enter username (%s): ' % _username)
    if not username:
        username = _username

    password = getpass.getpass('Enter password: ')

    with open(SC_CONF, 'w') as f:
        json.dump({'username': username, 'access_token': get_access_token(username, password)}, f)

    print 'Saved access_token.'


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    subparsers = parser.add_subparsers()

    upload_parser = subparsers.add_parser('upload', help='upload track to soundcloud')
    upload_parser.add_argument('filename', action='store', help='filename to upload')
    upload_parser.add_argument('--public', action='store_true', help='make track public')
    upload_parser.add_argument('--compress', action='store_true', help='compress file')
    upload_parser.add_argument('--no-compress', action='store_false', help='do not compress file')
    upload_parser.set_defaults(compress=True)
    upload_parser.add_argument('--downloadable', action='store_true', help='allow downloads')
    upload_parser.add_argument('--no-downloadable', action='store_false', help='disallow downloads')
    upload_parser.set_defaults(downloadable=True)
    upload_parser.add_argument('--bitrate', default=320, help='bitrate for compression')
    upload_parser.add_argument('--artist', help='id3 title')
    upload_parser.add_argument('--title', help='id3 title')
    upload_parser.add_argument('--album', help='id3 album')
    upload_parser.add_argument('--year', default=DEFAULT_YEAR, help='id3 year')
    upload_parser.add_argument('--description', help='description of track')
    upload_parser.add_argument('--genre', help='genre of track')
    upload_parser.add_argument('--tags', help='comma separated list of tags')
    upload_parser.add_argument('--artwork', help='artwork to use for song')
    upload_parser.set_defaults(command=command_upload)

    auth_parser = subparsers.add_parser('auth', help='Authenticate and save access token')
    auth_parser.set_defaults(command=command_auth)

    # default to upload command
    choices = subparsers.choices.keys()
    choices += ['-h', '--help', '-v', '--version']
    if sys.argv[1:] and sys.argv[1] not in choices:
        sys.argv = [sys.argv[0], 'upload'] + sys.argv[1:]

    args = parser.parse_args()
    args.command(args)
