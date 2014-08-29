from fit.types import Type


class Composite(Type):
    def __init__(self, base, **kwargs):
        super(Composite, self).__init__(base.number)
        self.base = base
        self.components=kwargs

    def read(self, read_buffer, architecture="<"):
        return self.base.read(read_buffer, architecture=architecture)

    def write(self, value):
        return self.base.write(value)


class ComponentField(object):
    def __init__(self, bits, offset=0):
        self.bits = bits
        self.offset = offset
        self.scale = None

    def __mul__(self, other):
        self.scale = other
        return self
