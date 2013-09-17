from .. import settings
import soundcloud

CLIENT_ID     = 'ffc80dc8b5bd435a15f9808724f73c40'
CLIENT_SECRET = 'b299b6681e00dfd9f5015639c7f5fe29'


def authenticate(username, password):
    client = soundcloud.Client(client_id=CLIENT_ID,
                               client_secret=CLIENT_SECRET,
                               username=username,
                               password=password,
                               scope='non-expiring')
    return client


def get_client(access_token=None):
    if not access_token:
        access_token = settings.access_token

    return soundcloud.Client(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token=access_token)
