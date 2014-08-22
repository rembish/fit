from struct import pack

from fit.record.definition import Definition


class RecordHeader(object):
    def __init__(self, local_message_type):
        self.type = local_message_type

    def __repr__(self):
        return '<%s[%d]>' % (
            self.__class__.__name__,
            self.type
        )

    @classmethod
    def read(cls, byte):
        msg_type = (byte >> 7) & 1

        if msg_type:
            return CompressedTimestampHeader.read(byte)
        return NormalHeader.read(byte)

    def write(self):
        raise NotImplementedError()

    def process_message(self, definitions, read_buffer):
        raise NotImplementedError()


class NormalHeader(RecordHeader):
    msg_type = None

    @classmethod
    def read(cls, byte):
        msg_type = (byte >> 6) & 1
        local_message_type = byte & 0b00001111  # 0-3 bits

        if msg_type:
            return DefinitionHeader(local_message_type)
        return DataHeader(local_message_type)

    def write(self):
        byte = 0 | (self.msg_type << 6) | self.type
        return pack("<B", byte)


class DefinitionHeader(NormalHeader):
    msg_type = 1

    def process_message(self, definitions, read_buffer):
        return Definition.read(
            definitions, header=self, read_buffer=read_buffer)


class DataHeader(NormalHeader):
    msg_type = 0

    def process_message(self, definitions, read_buffer):
        definition = definitions[self.type]
        return definition.build_message(read_buffer)


class CompressedTimestampHeader(RecordHeader):
    def __init__(self, local_message_type, time_offset):
        super(CompressedTimestampHeader, self).__init__(local_message_type)
        self.offset = time_offset

    def __repr__(self):
        return '<%s[%d] %+d>' % (
            self.__class__.__name__,
            self.type, self.offset
        )

    @classmethod
    def read(cls, byte):
        local_message_type = (byte >> 5) & 0b11  # 5-6 bits
        time_offset = byte & 0b00011111  # 0-4 bits
        return cls(local_message_type, time_offset)

    def write(self):
        byte = 1 | (self.type << 5) | self.offset
        return pack("<B", byte)

    def process_message(self, definitions, read_buffer):
        definition = definitions[self.type]
        return definition.build_message(read_buffer)
