from struct import unpack

from fit.types import KNOWN as KNOWN_TYPES

LITTLE_ENDIAN = 0
BIG_ENDIAN = 1


class Field(object):
    def __init__(self, chunk):
        self.id = ord(chunk[0])
        self.size = ord(chunk[1])
        self.type = KNOWN_TYPES[ord(chunk[2]) & 0b00011111]


class Record(object):
    compressed = 0

    def __init__(self, message_type):
        self.id = message_type

    @classmethod
    def open(cls, byte):
        if isinstance(byte, str):
            byte = ord(byte)

        compressed = byte & (1 << 7) != 1
        if not compressed:
            message_type = byte & (1 << 6)
            local_message_type = byte & 0b00001111

            if message_type:
                return DefinitionRecord(local_message_type)
            return DataRecord(local_message_type)

        local_message_type = byte & 0b01100000
        time_offset = byte & 0b00011111
        return CompressedDataRecord(local_message_type, offset=time_offset)


class DefinitionRecord(Record):
    def __init__(self, message_type):
        super(DefinitionRecord, self).__init__(message_type)
        self.architecture = LITTLE_ENDIAN
        self.type = None
        self.fields = None

    def build(self, stream):
        reserved, self.architecture = unpack("<BB", stream.read(2))
        self.type, field_count = unpack(
            "%sHB" % "<>"[self.architecture], stream.read(3))

        field_size = 3
        field_data = stream.read(field_size * field_count)
        for offset in range(0, len(field_data), field_size):
            chunk = field_data[offset:offset + field_size]
            self.fields.append(Field(chunk))


class DataRecord(Record):
    pass


class CompressedDataRecord(DataRecord):
    def __init__(self, message_type, offset):
        super(CompressedDataRecord, self).__init__(message_type)
        self.offset = offset
