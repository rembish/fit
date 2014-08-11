from io import BytesIO

from fit.record.header import RecordHeader


class Body(object):
    def read(self, chunk):
        size = len(chunk)
        buffer = BytesIO(chunk)

        while buffer.tell() != size:
            header = RecordHeader.read(ord(buffer.read(1)))
            message = header.construct(buffer)
            message.map(self)
