from ..settings import get_client

def share(track_url, users=None):
    """
    Returns list of users track has been shared with.
    """

    client = get_client()

    track = client.get('/resolve', url=track_url)

    if not users:
        return client.get('/tracks/%d/permissions' % track.id)

    permissions = {'user_id': []}
    for user in users.split(','):
        user = client.get('/resolve', url='http://soundcloud.com/%s' % user)
        permissions['user_id'].append(user.id)

    return client.put('/tracks/%d/permissions' % track.id, permissions=permissions)
