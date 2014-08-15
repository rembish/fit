from copy import copy
from io import BytesIO
from fit.message.common import FileId

from fit.record.definition import Definition, Fields
from fit.record.header import RecordHeader


class Body(list):
    def __init__(self, iterable=None):
        super(Body, self).__init__(iterable or [])

    def __repr__(self):
        return "<%s[%d]>" % (self.__class__.__name__, len(self))

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
            number = item.definition.number

            try:
                current = written.index(number)
            except ValueError:
                current = index
                index += 1
                written.append(number)

                chunks.append(item.definition.write(current))
            chunks.append(item.write(current))

        return "".join(chunks)

    @property
    def compressed(self):
        smallest = {}
        for item in self:
            number = item.definition.number
            compressed_definition = set(item.compressed_definition.fields)
            current = smallest.get(number, set())
            smallest[number] = current | compressed_definition

        new = Body()
        for item in self:
            number = item.definition.number
            current = copy(item)
            current.definition.fields = Fields(smallest[number])
            new.append(current)

        return new

    @property
    def file_id(self):
        if not self:
            return

        assert isinstance(self[0], FileId)
        return self[0]
