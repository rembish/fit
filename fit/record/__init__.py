class Record(object):
    def __init__(self, header):
        self.header = header

    @classmethod
    def read(cls, owner, header, buffer):
        raise NotImplementedError()
