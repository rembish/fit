from fit.structure.body import Body
from fit.structure.crc import Crc, compute_crc
from fit.structure.header import Header


class Writer(object):
    def __init__(self, fd, body=None):
        self.fd = fd

        self.header = Header()
        self.body = body or Body()
        self.crc = Crc()

    def write(self):
        chunk = self.body.write()
        self.header.data_size = len(chunk)
        self.crc.value = compute_crc(chunk)

        self.fd.seek(0)
        self.fd.truncate()

        self.fd.write(self.header.write())
        self.fd.write(chunk)
        self.fd.write(self.crc.write())