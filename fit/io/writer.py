from fit.structure.body import Body
from fit.structure.crc import Crc, compute_crc
from fit.structure.header import Header


class Writer(object):
    def __init__(self, fd, body=None):
        self.fd = fd

        self.header = Header()
        self.body = body or Body()
        self.crc = Crc()

    def __repr__(self):
        if not self.header or self.crc:
            self._prepare()

        return '<%s header=%r body=%r crc=%r>' % (
            self.__class__.__name__,
            self.header, self.body, self.crc
        )

    def _prepare(self):
        chunk = self.body.write()
        self.header.data_size = len(chunk)
        self.crc.value = compute_crc(chunk)
        return chunk

    def write(self):
        chunk = self._prepare()

        self.fd.seek(0)
        self.fd.truncate()

        self.fd.write(self.header.write())
        self.fd.write(chunk)
        self.fd.write(self.crc.write())
