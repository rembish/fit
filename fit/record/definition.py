from struct import unpack

from fit.record import Record


class Definition(Record):
    LITTLE = 0
    BIG = 1

    def __init__(self, header):
        super(Definition, self).__init__(header)
        self.byte_order = self.BIG
        self.number = None
        self.fields = Fields()

    @property
    def architecture(self):
        return {self.LITTLE: "<", self.BIG: ">"}.get(self.byte_order, "=")

    @classmethod
    def read(cls, header, buffer):
        instance = cls(header)
        reserved, instance.byte_order = unpack("<BB", buffer.read(2))
        instance.number, instance.fields.size = unpack(
            "%sHB" % instance.architecture, buffer.read(3))

        instance.fields.read(buffer)
        return instance
