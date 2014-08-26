from fit.types import Type, BinaryType


class Enum(Type):
    type = 0
    size = 1
    format = "B"
    variants = {}

    _invalid = 0xff

    def _load(self, data):
        return self.variants.get(data, data)

    def _save(self, value):
        for key, other in self.variants.items():
            if value == other:
                return key
        return value


class SInt8(BinaryType):
    type = 1
    size = 1
    format = "b"

    _invalid = 0x7f


class UInt8(BinaryType):
    type = 2
    size = 1
    format = "B"

    _invalid = 0xff


class SInt16(BinaryType):
    type = 3
    size = 2
    format = "h"

    _invalid = 0x7fff


class UInt16(BinaryType):
    type = 4
    size = 2
    format = "H"

    _invalid = 0xffff


class SInt32(BinaryType):
    type = 5
    size = 4
    format = "i"

    _invalid = 0x7fffffff


class UInt32(BinaryType):
    type = 6
    size = 4
    format = "I"

    _invalid = 0xffffffff


class String(Type):
    type = 7
    size = 1

    _invalid = 0x00

    def __init__(self, number, size=None):
        super(String, self).__init__(number, size=size)

    @property
    def format(self):
        return "%ds" % self.size


class Float32(Type):
    type = 8
    size = 4
    format = "f"

    _invalid = 0xffffffff


class Float64(Type):
    type = 9
    size = 8
    format = "d"

    _invalid = 0xffffffffffffffff


class UInt8Z(Type):
    type = 10
    size = 1
    format = "B"

    _invalid = 0x00


class UInt16Z(Type):
    type = 11
    size = 2
    format = "H"

    _invalid = 0x0000


class UInt32Z(Type):
    type = 12
    size = 4
    format = "I"

    _invalid = 0x00000000


class Byte(Type):
    type = 13
    size = 1

    def __init__(self, number, size=None, count=1):
        super(Byte, self).__init__(number, size=size)
        self.count = count
        self.format = "%dc" % self.count
        self._invalid = (1 << (count * self.size * 8)) - 1

    def __repr__(self):
        return "<%s[%d]x%d>" % (
            self.__class__.__name__,
            self.number, self.count
        )
