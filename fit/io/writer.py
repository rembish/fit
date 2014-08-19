from fit.structure.body import Body
from fit.structure.crc import Crc, compute_crc
from fit.structure.header import Header


class Writer(object):
    def __init__(self, ffd, body=None):
        self._fd = ffd

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

        self._fd.seek(0)
        self._fd.truncate()

        self._fd.write(self.header.write())
        self._fd.write(chunk)
        self._fd.write(self.crc.write())
