import os
import re
import subprocess
import sys

PROGRESS_RE = re.compile(r'\((\s?\d+)%\)')

class Progressbar(object):
    def __init__(self, filename=None):
        self.filename = filename

    def __call__(self, line):
        percent = int(PROGRESS_RE.search(line).groups()[0])
        bars    = percent / 2
        sys.stdout.write('\rencoding {0} [{1}{2}] {3}%'.format(self.filename, '=' * bars, ' ' * (50 - bars), percent))
        sys.stdout.flush()


def encode(filename, bitrate=320, callback=None):
    filename = os.path.expanduser(filename)

    # support CBR and VBR bitrate encoding
    if bitrate > 9:
        bitrate_switch = '-b'
    else:
        bitrate_switch = '-V'

    proc = subprocess.Popen(['lame', bitrate_switch, str(bitrate), filename, '--nohist'], stderr=subprocess.PIPE)

    start = False
    line = ''
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
            if callback:
                callback(line)
            line = ''
        elif buf == '':
            break

if __name__ == '__main__':
    encode('~/Desktop/honey.wav', callback=Progressbar('honey.wav'))
