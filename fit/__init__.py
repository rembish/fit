from fit.io.reader import Reader
from fit.io.writer import Writer
from fit.message import Message
from fit.structure.body import Body


class FitFile(object):
    def __init__(self, fd, records=None):
        self._fd = fd

        self.records = records or Body()

    @classmethod
    def open(cls, filename, mode='r'):
        if mode not in 'rwa':
            raise ValueError(
                "mode string must be one of 'r', 'w' or 'a', not '%s'" % mode)

        fd = open(filename, mode='%sb' % mode)

        records = None
        if mode in 'ar':
            records = Reader(fd).body

        return cls(fd, records=records)

    def __repr__(self):
        return "<%s '%s', mode '%s'>" % (
            self.__class__.__name__,
            self.name, self.mode
        )

    def __del__(self):
        return self.close()

    # File I/O methods

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_val:
            return self.close()

        raise exc_type, exc_val, exc_tb

    @property
    def mode(self):
        return self._fd.mode

    @property
    def name(self):
        return self._fd.name

    @property
    def closed(self):
        return self._fd.closed

    def fileno(self):
        return self._fd.fileno()

    def isatty(self):
        return self._fd.isatty()

    def readable(self):
        return self.mode[0] in 'ar'

    def seekable(self):
        return False

    def writable(self):
        return self.mode[0] in 'aw'

    def flush(self):
        if not self.writable():
            return

        Writer(self._fd, body=self.records).write()

    def close(self):
        if self.closed:
            return

        self.flush()
        self._fd.close()

    def minimize(self):
        self.records = self.records.compressed

    # FIT special methods
    def __getitem__(self, i):
        return self.records[i]

    def __setitem__(self, i, value):
        if not isinstance(value, Message):
            raise ValueError(value)

        self.records[i] = value

    def __delitem__(self, i):
        del self.records[i]

    def __iter__(self):
        for item in self.records:
            yield item
