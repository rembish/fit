# coding=utf-8
from fit.types.general import SInt32


class KnownMixin(object):
    known = {}

    def _load(self, data):
        return self.known.get(data, data)

    def _save(self, value):
        for key, other in self.known.items():
            if value == other:
                return key
        return value


def degrees(number):
    return SInt32(number, units="°") * (2 ** 31 / 180.)
