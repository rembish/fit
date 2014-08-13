from struct import unpack

from fit.messages import KNOWN as KNOWN_MESSAGES, make_generic
from fit.record import Record
from fit.types import KNOWN as KNOWN_TYPES


class Field(object):
    size = 3

    def __init__(self):
        self.definition = None
        self.type = -1

    @classmethod
    def read(cls, chunk):
        instance = cls()
        instance.definition = ord(chunk[0])

        base_type = ord(chunk[2]) & 0b00011111
        instance.type = KNOWN_TYPES[base_type]

        assert ord(chunk[1]) == instance.type.size
        assert base_type == instance.type.type

        return instance


class Fields(list):
    def __init__(self):
        super(Fields, self).__init__()

    @property
    def size(self):
        return sum(map(lambda x: x.type.size, self))

    def read(self, chunk):
        for offset in range(0, len(chunk), Field.size):
            self.append(Field.read(chunk[offset:offset + Field.size]))


class Definition(Record):
    LITTLE = 0
    BIG = 1

    def __init__(self, header):
        super(Definition, self).__init__(header)
        self.byte_order = self.BIG
        self.number = None
        self.fields = Fields()

    @property
    def architecture(self):
        return {self.LITTLE: "<", self.BIG: ">"}.get(self.byte_order, "=")

    @classmethod
    def read(cls, owner, header, buffer):
        instance = cls(header)
        reserved, instance.byte_order = unpack("<BB", buffer.read(2))
        instance.number, fields_count = unpack(
            "%sHB" % instance.architecture, buffer.read(3))

        chunk = buffer.read(fields_count * Field.size)
        instance.fields.read(chunk)

        owner.definitions[instance.header.type] = instance
        return instance

    def build_message(self, buffer):
        message = KNOWN_MESSAGES.get(self.number, make_generic(self.fields))
        record = message.read(buffer)
        return record
