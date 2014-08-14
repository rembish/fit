from io import FileIO

from fit.file import FitFile
from fit.reader import Reader


def open(filename, mode='r'):
    if mode not in 'rwa':
        raise ValueError(
            "mode string must be one of 'r', 'w' or 'a', not '%s'" % mode)

    fd = FileIO(filename, mode='%sb' % mode)

    records = None
    if mode in 'ar':
        records = Reader(fd).body

    return FitFile(fd, records=records)
