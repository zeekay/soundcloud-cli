import os
import sys
from io import BytesIO
import requests

from .. import settings


class CancelledError(Exception):
    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, msg)

    def __str__(self):
        return self.msg

    __repr__ = __str__


class BufferReader(BytesIO):
    def __init__(self, buf=b'', callback=None):
        self._callback = callback
        self._progress = 0
        self._len = len(buf)
        BytesIO.__init__(self, buf)

    def __len__(self):
        return self._len

    def read(self, n=-1):
        chunk = BytesIO.read(self, n)
        self._progress += int(len(chunk))

        if self._callback:
            try:
                self._callback(self._len, self._progress)
            except Exception as e:
                print e
                raise CancelledError('The upload was cancelled.')
        return chunk


class Progressbar(object):
    def __init__(self, filename=None):
        self.filename = filename
        self.done = False

    def __call__(self, total=None, uploaded=None):
        if self.done:
            return

        done = uploaded / float(total)
        bars = int(50 * done)
        percent = int(100 * done)

        sys.stdout.write('\ruploading {0} [{1}{2}] {3}%'.format(self.filename, '=' * bars, ' ' * (50 - bars), percent))
        sys.stdout.flush()


def upload(filename, sharing='private', downloadable=True, title=None, description=None, genre=None, tag_list=None, artwork=None, callback=Progressbar):
    if not title:
        title = os.path.splitext(os.path.basename(filename))[0]

    filename = os.path.expanduser(filename)

    data = {
        'oauth_token': settings.access_token,
        'track[asset_data]': (filename, open(filename, 'rb').read()),
        'track[sharing]': sharing,
        'track[downloadable]': downloadable,
        'track[title]': title,
    }

    if description:
        data['track[description]'] = description

    if genre:
        data['track[genre]'] = genre

    if tag_list:
        data['track[tag_list]'] = ' '.join(tag_list)

    if artwork:
        artwork = os.path.expanduser(artwork)
        data['track[artwork_data'] = (artwork, open(artwork, 'rb').read())

    (data, content_type) = requests.packages.urllib3.filepost.encode_multipart_formdata(data)

    headers = {
        "Content-Type": content_type
    }

    body = BufferReader(data, callback=callback(', '.join(os.path.basename(f) for f in [filename, artwork] if f)))

    res = requests.post('https://api.soundcloud.com/tracks.json', data=body, headers=headers)
    print

    if res.ok:
        res = res.json()
    else:
        print res.status_code
        print res.headers
        print res.text
        return

    if sharing == 'private':
        secret_token = res['secret_uri'].split('secret_token=')[1]
        res['permalink_url'] = res['permalink_url'] + '/' + secret_token

    return res
