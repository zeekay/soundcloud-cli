from .. import settings
from .client import get_client


def list(username=None):
    client = get_client()

    if not username:
        user_id = settings.user.get('id', None)
    else:
        user = settings.users.get(username, None)
        if not user:
            user = client.get('/resolve', url='https://soundcloud/%s' % username)
            user_id = user.id

    page_size = 100
    offset    = 0

    return client.get('/users/%d/tracks' % user_id, order='created_at', limit=page_size, offset=offset)
