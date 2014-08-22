from struct import pack

from fit.types import KNOWN as KNOWN_TYPES


class Fields(list):
    field_size = 3

    def __init__(self, iterable=None):
        super(Fields, self).__init__(iterable or [])

    def __repr__(self):
        return '<%s%s>' % (
            self.__class__.__name__,
            super(Fields, self).__repr__()
        )

    @property
    def size(self):
        return sum(field.size for field in self)

    def read(self, data):
        for offset in range(0, len(data), self.field_size):
            chunk = data[offset:offset + self.field_size]

            base_type = ord(chunk[2]) & 0b00011111
            number = ord(chunk[0])
            size = ord(chunk[1])

            field = KNOWN_TYPES[base_type](number, size=size)
            self.append(field)

    def write(self):
        chunks = []
        for field in self:
            endian = int(field.size > 1)
            base_type = (endian << 7) | field.type
            chunks.append(pack("<BBB", field.number, field.size, base_type))
        return "".join(chunks)
