from fit.types import Type


class Array(Type):
    def __init__(self, value_type, size=None):
        super(Array, self).__init__(value_type.number, size=size)
        self.value_type = value_type

    def __repr__(self):
        return "<%s: %rx%d>" % (
            self.__class__.__name__, self.value_type, self.count
        )

    @property
    def count(self):
        return self.size / self.value_type.size

    def read(self, read_buffer, architecture="<"):
        values = []
        for _ in range(self.count):
            values.append(self.value_type.read(
                read_buffer, architecture=architecture))
        return values

    def write(self, values):
        return "".join(self.value_type.write(value) for value in values)
