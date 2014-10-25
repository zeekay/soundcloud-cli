import os
import sys

from . import settings, utils


def print_shared_with(users):
    print 'shared with:'
    for user in users:
        print '  {0} ({0})'.format(user.permalink, user.permalink_url)


def command_auth(args):
    import getpass
    from .api.client import authenticate

    # try to detect username
    username = settings.user.get('name', None)
    if not username:
        username = getpass.getuser()

    # read username
    user_input = raw_input('enter username ({0}): '.format(username))
    if user_input:
        username = user_input

    # read password
    password = getpass.getpass('enter password: ')

    # authenticate with username/password
    client = authenticate(username, password)

    # get user info
    me = client.get('/me')

    # save settings
    settings.access_token = client.access_token
    settings.user         = me.obj
    settings.user['name'] = me.username
    settings.save()
    print 'authenticated as {0}.'.format(me.username)


def command_defaults(args):
    key   = args.key
    value = args.value

    known_defaults = {
        'share_with': lambda v: [u.strip() for u in v.split(',')],
        'bitrate': lambda v: int(v),
    }

    if known_defaults.get(key, None):
        value = known_defaults[key](value)

    settings.defaults[key] = value
    settings.save()
    print 'set {0} = {1}'.format(key, str(value))


@utils.require_auth
def command_list(args):
    from .api.list import list
    from .api.client import get_client

    client   = get_client()
    username = args.username

    if not username:
        user_id  = settings.user.get('id')
        username = settings.user.get('name')
    else:
        user = settings.users.get(username, None)
        if user:
            user_id  = user['id']
        else:
            user = client.get('/resolve', url='https://soundcloud/{0}'.format(username))
            user_id = user.id

    tracks = list(user_id)

    # find longest title to build formatting string
    title_len = max(len(t.title) for t in tracks)
    format_spec = "  {{0:<{0}}} {{1}}".format(title_len + 2)

    print 'tracks by {0}:'.format(username)
    for track in tracks:
        print format_spec.format(track.title, track.permalink_url)


@utils.require_auth
def command_share(args):
    from .api.share import share

    if args.users:
        users = [u.strip() for u in args.users.split(',')]
    else:
        users = []

    users = share(url=args.track_url, users=users)
    print_shared_with(users)


@utils.require_auth
def command_upload(args):
    from .api.upload import upload
    from .api.share import share

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
    else:
        tag_list = None

    res = upload(args.filename, sharing=sharing,
                                downloadable=args.downloadable,
                                title=args.title,
                                description=args.description,
                                genre=args.genre,
                                tag_list=tag_list,
                                artwork=args.artwork)

    url = res['permalink_url']

    print url
    utils.open_browser(url)
    utils.copy_to_clipboard(url)

    # share if defaults.share_with set or if requested explicitly
    share_with = settings.defaults.get('share_with', None)

    if args.share_with:
        share_with = [x.strip() for x in args.share_with.split(',')]

    if share_with:
        users = share(track_id=res['id'], users=share_with)
        print_shared_with(users)


def main():
    import argparse

    from __init__ import __version__

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    subparsers = parser.add_subparsers()

    auth_parser = subparsers.add_parser('auth', help='authenticate and save access token')
    auth_parser.set_defaults(command=command_auth)

    defaults_parser = subparsers.add_parser('defaults', help='configure defaults')
    defaults_parser.add_argument('key', help='key')
    defaults_parser.add_argument('value', help='value')
    defaults_parser.set_defaults(command=command_defaults)

    list_parser = subparsers.add_parser('list', help='list tracks for given user')
    list_parser.add_argument('username', nargs='?', help='key')
    list_parser.set_defaults(command=command_list)

    share_parser = subparsers.add_parser('share', help='share track with users')
    share_parser.add_argument('track_url', help='track you want to share')
    share_parser.add_argument('users', nargs='?', help='users you want to share track with')
    share_parser.set_defaults(command=command_share)

    upload_parser = subparsers.add_parser('upload', help='upload track to soundcloud')
    upload_parser.add_argument('filename', help='filename to upload')
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

    try:
        args.command(args)
    except KeyboardInterrupt:
        print
        sys.exit(1)
