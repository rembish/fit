from struct import unpack, pack

from fit.utils import get_known


class Type(object):
    type = None
    size = 0
    format = "x"

    _invalid = None

    def __init__(self, number, size=None):
        self.number = number
        self.size = size or self.__class__.size

    def __eq__(self, other):
        return self.number == other.number

    def __repr__(self):
        return '<%s[%d]>' % (
            self.__class__.__name__, self.number
        )

    def read(self, read_buffer, architecture="<"):
        data = unpack("%(arch)s%(format)s" % {
            "arch": architecture,
            "format": self.format
        }, read_buffer.read(self.size))[0]

        if data == self._invalid:
            data = None

        return data

    def write(self, value):
        return pack(
            "<%s" % self.format,
            value if value is not None else self._invalid)

    def _load(self, data):
        return data

    def _save(self, value):
        return value


class BinaryType(Type):
    def __init__(self, number, size=None, units=None):
        super(BinaryType, self).__init__(number, size=size)
        self.units = units
        self.scale = None
        self.offset = None

    def __mul__(self, other):
        if isinstance(other, (int, long, float)):
            self.scale = other
        if isinstance(other, (str, unicode)):
            self.units = other
        return self

    def __rmul__(self, other):
        self.scale = other
        return self

    def __sub__(self, other):
        self.offset = -other
        return self

    def __add__(self, other):
        self.offset = other
        return self

    def _load(self, data):
        if not self.scale and not self.offset:
            return super(BinaryType, self)._load(data)

        value = float(data)
        if self.scale:
            value /= float(self.scale)
        if self.offset:
            value -= float(self.offset)
        return value

    def _save(self, value):
        if not self.scale and not self.offset:
            return super(BinaryType, self)._save(value)

        data = value
        if self.offset:
            data += self.offset
        if self.scale:
            data *= self.scale
        return int(data)


KNOWN = get_known(__name__, Type)
