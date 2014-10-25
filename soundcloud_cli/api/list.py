from .client import get_client


def list(user_id):
    client = get_client()

    page_size = 100
    offset    = 0

    return client.get('/users/{0}/tracks'.format(user_id), order='created_at',
                                                           limit=page_size,
                                                           offset=offset)
