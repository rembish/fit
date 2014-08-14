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

                if number not in self.definitions:  # FIXME
                    self.definitions[number] = item._definition

                self.definitions[number].write(current)
            chunks.append(item.write(current))

        return "".join(chunks)
