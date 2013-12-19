import os
import re
import subprocess
import sys

from datetime import date
from . import settings

DEFAULT_YEAR  = date.today().year
PROGRESS_RE = re.compile(r'\((\s?\d+)%\)')


class Progressbar(object):
    def __init__(self, filename=None):
        self.filename = filename

    def __call__(self, line):
        percent   = int(PROGRESS_RE.search(line).groups()[0])
        bars      = percent / 2
        done      = '=' * bars
        remaining = ' ' * (50 - bars)

        sys.stdout.write('\rcompressing {0} [{1}{2}] {3}%'.format(self.filename, done, remaining, percent))
        sys.stdout.flush()


def compress(filename, artist='', title='', album='', year='', bitrate=320, callback=Progressbar):
    if artist is None:
        artist = settings.username

    if title is None:
        title = os.path.splitext(os.path.basename(filename))[0]

    if album is None:
        album = 'work in progress'

    if year is None:
        year = DEFAULT_YEAR

    # expand possible tilde
    filename = os.path.expanduser(filename)

    # support CBR and VBR bitrate encoding
    if bitrate > 9:
        bitrate_switch = '-b'
    else:
        bitrate_switch = '-V'

    args = [
        'lame',
        '--nohist',
        bitrate_switch, str(bitrate),
        '--tt', title,
        '--ta', artist,
        '--tl', album,
        '--ty', str(year),
        filename
    ]

    proc = subprocess.Popen(args, stderr=subprocess.PIPE)

    start = False
    line = ''
    callback = callback(filename=os.path.basename(filename))

    while True:
        if not start:
            buf = proc.stderr.read(1)
            if buf == '\r':
                start = True
                proc.stderr.read(153)
            continue

        buf = proc.stderr.read(1)
        line += buf
        if buf == '\r':
            callback(line)
            line = ''
        elif buf == '':
            break
