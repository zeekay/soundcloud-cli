from .. import settings
from .client import get_client


def share(track_id=None, url=None, users=None):
    """
    Returns list of users track has been shared with.
    Either track or url need to be provided.
    """

    client = get_client()

    if url:
        track_id = client.get('/resolve', url=url).id

    if not users:
        return client.get('/tracks/%d/permissions' % track_id)

    permissions = {'user_id': []}

    for username in users:
        # check cache for user
        user = settings.users.get(username, None)
        if user:
            permissions['user_id'].append(user['id'])
        else:
            user = client.get('/resolve', url='http://soundcloud.com/%s' % username)
            permissions['user_id'].append(user.id)
            settings.users[username] = user.obj
    settings.save()

    return client.put('/tracks/%d/permissions' % track_id, permissions=permissions)
