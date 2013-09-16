import json
import os
import sys
from datetime import date

import soundcloud

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

    os.system('lame -b %d --tt "%s" --ta "%s" --tl "%s" --ty %s %s' % (bitrate, title, artist, album, year, filename))


def upload_gen(filename):
    """
    Wrap a file in a progress bar and spit out progress as it's uploaded.
    """
    with open(filename, 'rb') as f:
        uploaded = 0
        f.seek(0, 2)
        total = f.tell()
        total_mb = float(total) / 1024 / 1024
        f.seek(0)

        for data in f:
            uploaded += len(data)
            uploaded_mb = float(uploaded) / 1024 / 1024
            done = int(50 * uploaded / total)
            sys.stdout.write("\r[%s%s] %.2f / %.2f" % ('=' * done, ' ' * (50 - done), uploaded_mb, total_mb))
            sys.stdout.flush()
            yield data
        print


def upload_track(filename, title=None, sharing='private'):
    filename = os.path.expanduser(filename)
    client = get_client()

    if not title:
        title = os.path.splitext(os.path.basename(filename))[0]

    print 'uploading {0}...'.format(filename)

    track = client.post('/tracks', track={
        'title': title,
        'asset_data': open(filename, 'rb'),
        'sharing': sharing,
    })

    if sharing == 'private':
        secret_token = track.secret_uri.split('secret_token=')[1]
        track.permalink_url = track.permalink_url + '/' + secret_token

    return track


def command_upload(args):
    if not args.no_compress and args.filename.endswith('.wav'):
        print 'compressing file...'
        compress_track(args.filename, bitrate=args.bitrate,
                                      title=args.title,
                                      artist=args.artist,
                                      album=args.album,
                                      year=args.year)

        args.filename.replace('.wav', '.mp3')

    if args.public:
        sharing = 'public'
    else:
        sharing = 'private'

    track = upload_track(args.filename, title=args.title, sharing=sharing)
    print track.permalink_url


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
    subparsers = parser.add_subparsers()

    upload_parser = subparsers.add_parser('upload', help='Upload track to soundcloud')
    upload_parser.add_argument('filename', action='store', help='File to upload')
    upload_parser.add_argument('--public', action='store_true', help='Make track public')
    upload_parser.add_argument('--no-compress', action='store_true', help='Compress file')
    upload_parser.add_argument('--bitrate', default=320, help='Compress file')
    upload_parser.add_argument('--tags', help='Tags for track')
    upload_parser.add_argument('--artist', help='id3 title')
    upload_parser.add_argument('--title', help='id3 title')
    upload_parser.add_argument('--album', help='id3 album')
    upload_parser.add_argument('--year', default=DEFAULT_YEAR, help='id3 year')
    upload_parser.set_defaults(command=command_upload)

    auth_parser = subparsers.add_parser('auth', help='Authenticate and save access token')
    auth_parser.set_defaults(command=command_auth)

    # default to upload command
    if sys.argv[1:] and sys.argv[1] not in subparsers.choices:
        sys.argv = [sys.argv[0], 'upload'] + sys.argv[1:]

    args = parser.parse_args()
    args.command(args)

if __name__ == '__main__':
    main()
