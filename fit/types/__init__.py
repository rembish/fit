from importlib import import_module
from inspect import getmembers, isclass
from pkgutil import iter_modules
from struct import unpack, pack


class Type(object):
    type = -1
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

    def read(self, buffer, architecture="="):
        data = unpack("%(arch)s%(format)s" % {
            "arch": architecture,
            "format": self.format
        }, buffer.read(self.size))[0]

        if data == self._invalid:
            data = None

        return data

    def write(self, value):
        if value is None:
            value = self._invalid
        return pack("<%s" % self.format, value)

    def readable(self, value):
        if hasattr(self, "known"):
            return self.known.get(value, value)
        return value


def get_known():
    main = import_module(__name__)
    known = {}

    for _, module_name, _ in iter_modules(main.__path__, "%s." % __name__):
        module = import_module(module_name)
        for _, obj in getmembers(module, isclass):
            if issubclass(obj, Type):
                known[obj.type] = obj

    return known


KNOWN = get_known()
del get_known
