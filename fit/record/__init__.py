class Record(object):
    def __init__(self, header):
        self.header = header

    @classmethod
    def read(cls, header, buffer):
        raise NotImplementedError()

    def map(self, owner):
        raise NotImplementedError()
