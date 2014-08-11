from fit.record.data import Data
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
        type = byte & (1 << 7)

        if type:
            return CompressedTimestampHeader.read(byte)
        return NormalHeader.read(byte)

    def construct(self, buffer):
        raise NotImplementedError()


class NormalHeader(RecordHeader):
    @classmethod
    def read(cls, byte):
        type = byte & (1 << 6)
        local_message_type = byte & 0b00001111  # 0-3 bits

        if type:
            return DefinitionHeader(local_message_type)
        return DataHeader(local_message_type)


class DefinitionHeader(NormalHeader):
    def construct(self, buffer):
        return Definition.read(self, buffer)


class DataHeader(NormalHeader):
    def construct(self, buffer):
        return Data.read(self, buffer)


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
        local_message_type = byte & 0b01100000  # 5-6 bits
        time_offset = byte & 0b00011111  # 0-4 bits
        return cls(local_message_type, time_offset)
