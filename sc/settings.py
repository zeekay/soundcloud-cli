import json
import os
import sys

import soundcloud

CLIENT_ID     = 'ffc80dc8b5bd435a15f9808724f73c40'
CLIENT_SECRET = 'b299b6681e00dfd9f5015639c7f5fe29'
SC_CONF = os.path.expanduser('~/.sc')


def get_access_token(username, password):
    client = soundcloud.Client(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        username=username,
        password=password,
        scope='non-expiring',
    )

    return client.access_token


def auth(username, password):
    with open(SC_CONF, 'w') as f:
        access_token = get_access_token(username, password)
        json.dump({'username': username, 'access_token': access_token}, f)


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
