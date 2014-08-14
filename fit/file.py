from fit.body import Body
from fit.messages import Message
from fit.writer import Writer


class FitFile(object):
    def __init__(self, fd, records=None):
        self._fd = fd

        self.records = records or Body()
        self._changed = False

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

        writer = Writer(self._fd)
        writer.body = self.records
        writer.write()

    def close(self):
        self.flush()
        self._fd.close()

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
