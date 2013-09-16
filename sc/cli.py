import json
import sys
from sc import get_settings, compress_track, get_access_token, DEFAULT_YEAR, SC_CONF
from upload import upload
from utils import copy_to_clipboard, open_browser
from __init__ import __version__

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


    url = res['permalink_url']

    print url
    copy_to_clipboard(url)
    open_browser(url)


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

    auth_parser = subparsers.add_parser('auth', help='authenticate and save access token')
    auth_parser.set_defaults(command=command_auth)

    # default to upload command
    if sys.argv[1:]:
        choices = subparsers.choices.keys()
        choices += ['-h', '--help', '-v', '--version']

        # unless recognized command is passed, treat first argument as file to upload
        if sys.argv[1] not in choices:
            sys.argv = [sys.argv[0], 'upload'] + sys.argv[1:]

    args = parser.parse_args()
    args.command(args)
