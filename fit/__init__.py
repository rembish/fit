from contextlib import closing
from io import FileIO

from fit.reader import Reader


def open(filename, mode='r'):
    if mode not in 'rwa':
        raise ValueError(
            "mode string must be one of 'r', 'w' or 'a', not '%s'" % mode)

    with closing(FileIO(filename, mode='%sb' % mode)) as fd:
        if mode == 'r':
            return Reader(fd)
