from io import BytesIO

from fit.record.header import RecordHeader


class Body(list):
    def __init__(self):
        super(Body, self).__init__()
        self.definitions = {}

    def read(self, chunk):
        size = len(chunk)
        buffer = BytesIO(chunk)

        while buffer.tell() != size:
            header = RecordHeader.read(ord(buffer.read(1)))
            header.process_message(self, buffer)
