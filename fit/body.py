from io import BytesIO

from fit.record.definition import Definition
from fit.record.header import RecordHeader


class Body(list):
    def __init__(self):
        super(Body, self).__init__()

    def read(self, chunk):
        size = len(chunk)
        buffer = BytesIO(chunk)
        definitions = {}

        while buffer.tell() != size:
            header = RecordHeader.read(ord(buffer.read(1)))
            message = header.process_message(definitions, buffer)

            if not isinstance(message, Definition):
                self.append(message)

    def write(self):
        index = 0
        written = []
        chunks = []

        for item in self:
            number = item._definition.number

            try:
                current = written.index(number)
            except ValueError:
                current = index
                index += 1
                written.append(number)

                chunks.append(item._definition.write(current))
            chunks.append(item.write(current))

        return "".join(chunks)
