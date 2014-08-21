from copy import copy

from fit.io.reader import Reader
from fit.io.writer import Writer
from fit.messages import Message
from fit.files import KNOWN as KNOWN_FILES, FileLike
from fit.structure.body import Body


class FitFile(FileLike):
    def __init__(self, ffd, body=None):
        self._fd = ffd

        self.body = body or Body()
        self._apply_mixin()

    @classmethod
    def open(cls, filename, mode='r'):
        if mode not in 'rwa':
            raise ValueError(
                "mode string must be one of 'r', 'w' or 'a', not '%s'" % mode)

        ffd = open(filename, mode='%sb' % 'w' if mode == 'w' else 'r')

        body = None
        if mode in 'ar':
            body = Reader(ffd).body

        if mode == 'a':
            ffd.close()
            ffd = open(filename, mode='ab')

        return cls(ffd, body=body)

    def __repr__(self):
        return "<%s '%s', mode '%s'>" % (
            self.__class__.__name__,
            self.name, self.mode[0]
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

    def write(self):
        if not self.writable():
            raise IOError("File not open for writing")
        Writer(self._fd, body=self.body).write()

    def flush(self):
        if self.writable():
            self.write()

    def close(self):
        if self.closed:
            return

        self.flush()
        self._fd.close()

    def minimize(self):
        self.body = self.body.compressed

    # List special methods

    def __getitem__(self, i):
        return self.body[i]

    def __setitem__(self, i, value):
        self._validate(i, value)
        self.body[i] = value
        self._apply_mixin()

    def __delitem__(self, i):
        self._validate(i)
        del self.body[i]
        self._apply_mixin()

    def __iter__(self):
        for item in self.body:
            yield item

    def __len__(self):
        return len(self.body)

    def append(self, value):
        self._validate(len(self), value)
        self.body.append(value)
        self._apply_mixin()

    def extend(self, values):
        for value in values:
            self.append(value)

    def remove(self, i):
        self._validate(i)
        self.body.remove(i)
        self._apply_mixin()

    def pop(self, i=0):
        self._validate(i)
        value = self.body.pop(i)
        self._apply_mixin()
        return value

    def index(self, i):
        return self.body.index(i)

    def copy(self, other=None):
        if not other:
            return copy(self.body)

        assert isinstance(other, FitFile)
        self.body = other.copy()
        self._apply_mixin()


def register(file_cls):
    if not issubclass(file_cls, FitFile):
        raise ValueError(
            "%s should be subclass of FitFile" % file_cls.__name__)
    if not isinstance(file_cls.type, int):
        raise ValueError(
            "%s should have defined file type" % file_cls.__name__)

    KNOWN_FILES[file_cls.type] = file_cls
