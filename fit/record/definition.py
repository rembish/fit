from copy import copy
from struct import unpack, pack

from fit.messages import KNOWN as KNOWN_MESSAGES
from fit.messages.generic import GenericMessage
from fit.record.fields import Fields


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
        return {self.LITTLE: "<", self.BIG: ">"}.get(self.byte_order, "<")

    @classmethod
    def read(cls, definitions, header, read_buffer):
        instance = cls(header)
        _, instance.byte_order = unpack("<BB", read_buffer.read(2))
        instance.number, fields_count = unpack(
            "%sHB" % instance.architecture, read_buffer.read(3))

        chunk = read_buffer.read(fields_count * Fields.field_size)
        instance.fields.read(chunk)

        definitions[instance.header.type] = instance
        return instance

    def write(self, index):
        from fit.record.header import DefinitionHeader
        chunk = pack("<BBHB", 0, self.LITTLE, self.number, len(self.fields))
        return DefinitionHeader(index).write() + chunk + self.fields.write()

    def build_message(self, read_buffer):
        message_cls = KNOWN_MESSAGES.get(self.number, GenericMessage)
        message = message_cls(copy(self))
        if isinstance(message, GenericMessage):
            message.msg_type = self.number

        message.read(read_buffer, copy(self.fields))
        return message
