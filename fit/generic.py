from contextlib import closing
from struct import unpack

from fit.helper import Header
from fit.messages import FileIdMessage


class FitFile(object):
    def __init__(self):
        pass

    @classmethod
    def open(cls, filename):
        with closing(open(filename, 'rb')) as fp:
            return cls.openfp(fp)

    @classmethod
    def openfp(cls, fp):
        # 1. read header size

        fp.seek(0)
        header_size = ord(fp.read(1))

        if header_size < 12:
            raise Exception()  # FIXME

        header = Header(fp.read(header_size))
        if not header.valid():
            raise Exception()  # FIXME

        # 2. searching for file_id record to define current file type

        record_header = ord(fp.read(1))
        record_type = record_header & (1 << 7)
        # First record should be normal data message
        if record_type:
            raise Exception()  # FIXME

        reserved, architecture = unpack("<BB", fp.read(2))
        architecture = ">" if architecture else "<"
        global_message_number, number_of_fields = \
            unpack("%sHB" % architecture, fp.read(3))

        # First record should be FileId
        if global_message_number != FileIdMessage.get_type():
            raise Exception()  # FIXME

        field_size = 3
        fields_data = fp.read(field_size * number_of_fields)
        for i, offset in enumerate(range(0, len(fields_data), field_size)):
            chunk = fields_data[offset:offset + field_size]
