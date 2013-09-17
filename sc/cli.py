import os
import sys

from . import settings
from .utils import copy_to_clipboard, open_browser


def command_auth(args):
    import getpass
    from .api.client import get_access_token

    _username = getpass.getuser()
    username = raw_input('Enter username (%s): ' % _username)
    if not username:
        username = _username

    password = getpass.getpass('Enter password: ')

    settings.access_token = get_access_token(username, password)
    settings.username = username
    settings.save()
    print 'Saved access_token.'


def command_share(args):
    from .api.share import share

    users = share(args.track_url, args.users)

    print 'shared with:'
    for user in users:
        print '  %s (%s)' % (user.permalink, user.permalink_url)
    return


def command_upload(args):
    from .api.upload import upload

    if args.compress and args.filename.endswith('.wav'):
        from .lame import compress

        compress(args.filename, bitrate=args.bitrate,
                                title=args.title,
                                artist=args.artist,
                                album=args.album,
                                year=args.year)
        # clear line
        rows, columns = os.popen('stty size', 'r').read().split()
        sys.stdout.write('\r' + ' ' * int(columns))

        args.filename = args.filename.replace('.wav', '.mp3')

    if args.public:
        sharing = 'public'
    else:
        sharing = 'private'

    if args.tags:
        tag_list = [x.strip() for x in args.tags.split(',')]

    if args.share_with:
        share_with = [x.strip() for x in args.share_with.split(',')]

    res = upload(args.filename, sharing=sharing,
                                downloadable=args.downloadable,
                                title=args.title,
                                description=args.description,
                                genre=args.genre,
                                tag_list=tag_list,
                                share_with=share_with,
                                artwork=args.artwork)

    url = res['permalink_url']

    print url
    open_browser(url)
    copy_to_clipboard(url)


def main():
    import argparse

    from __init__ import __version__

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    subparsers = parser.add_subparsers()

    auth_parser = subparsers.add_parser('auth', help='authenticate and save access token')
    auth_parser.set_defaults(command=command_auth)

    share_parser = subparsers.add_parser('share', help='share track with users')
    share_parser.add_argument('track_url', action='store', help='track you want to share')
    share_parser.add_argument('users', action='store', nargs='?', help='users you want to share track with')
    share_parser.set_defaults(command=command_share)

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
    upload_parser.add_argument('--year', help='id3 year')
    upload_parser.add_argument('--description', help='description of track')
    upload_parser.add_argument('--genre', help='genre of track')
    upload_parser.add_argument('--tags', help='comma separated list of tags')
    upload_parser.add_argument('--share-with', help='comma separated list of users to share with')
    upload_parser.add_argument('--artwork', help='artwork to use for song')
    upload_parser.set_defaults(command=command_upload)

    # default to upload command
    if sys.argv[1:]:
        choices = subparsers.choices.keys()
        choices += ['-h', '--help', '-v', '--version']

        # unless recognized command is passed, treat first argument as file to upload
        if sys.argv[1] not in choices:
            sys.argv = [sys.argv[0], 'upload'] + sys.argv[1:]

    args = parser.parse_args()
    args.command(args)
