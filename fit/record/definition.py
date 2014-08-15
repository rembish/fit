from struct import unpack, pack

from fit.message import KNOWN as KNOWN_MESSAGES, GenericMessage
from fit.type import KNOWN as KNOWN_TYPES


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
        return sum(map(lambda x: x.type.size, self))

    def read(self, data):
        for offset in range(0, len(data), self.field_size):
            chunk = data[offset:offset + self.field_size]

            base_type = ord(chunk[2]) & 0b00011111
            number = ord(chunk[0])
            size = ord(chunk[1])

            field = KNOWN_TYPES[base_type](number, length=size)
            self.append(field)

    def write(self):
        chunks = []
        for field in self:
            endian = int(field.size > 1)
            base_type = (endian << 7) | field.type
            chunks.append(pack(
                "<BBB", field.number, field._length or field.size, base_type))
        return "".join(chunks)


class Definition(object):
    LITTLE = 0
    BIG = 1

    def __init__(self, header):
        self.header = header
        self.byte_order = self.BIG
        self.number = None
        self.fields = Fields()

    def __repr__(self):
        return '<%s[%d] with %r>' % (
            self.__class__.__name__,
            self.number,
            self.fields
        )

    @property
    def architecture(self):
        return {self.LITTLE: "<", self.BIG: ">"}.get(self.byte_order, "=")

    @classmethod
    def read(cls, definitions, header, buffer):
        instance = cls(header)
        reserved, instance.byte_order = unpack("<BB", buffer.read(2))
        instance.number, fields_count = unpack(
            "%sHB" % instance.architecture, buffer.read(3))

        chunk = buffer.read(fields_count * Fields.field_size)
        instance.fields.read(chunk)

        definitions[instance.header.type] = instance
        return instance

    def write(self, index):
        from fit.record.header import DefinitionHeader
        chunk = pack("<BBHB", 0, self.LITTLE, self.number, len(self.fields))
        return DefinitionHeader(index).write() + chunk + self.fields.write()

    def build_message(self, buffer):
        message_cls = KNOWN_MESSAGES.get(self.number, GenericMessage)
        message = message_cls(self)
        if isinstance(message, GenericMessage):
            message.msg_type = self.number

        message.read(buffer)
        return message
