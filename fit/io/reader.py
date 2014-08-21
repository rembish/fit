from os import fstat

from fit.structure.body import Body
from fit.structure.crc import Crc, compute_crc
from fit.structure.header import Header
from fit.exceptions import HeaderFormatError, BodyFormatError, CrcFormatError


class Reader(object):
    def __init__(self, ffd):
        self._fd = ffd

        self._header = Header()
        self._body = Body()
        self._crc = Crc()

        self.file_size = fstat(self._fd.fileno()).st_size
        self.header_chunk = ""

    def __repr__(self):
        return '<%s header=%r body=%r crc=%r>' % (
            self.__class__.__name__,
            self.header, self.body, self.crc
        )

    @property
    def header(self):
        if self._header:
            return self._header

        self._fd.seek(0)

        header_size = ord(self._fd.read(1))
        if header_size not in (12, 14):
            raise HeaderFormatError(
                "Strange size: %d bytes" % header_size)

        header = self._fd.read(header_size - 1)
        if len(header) != header_size - 1:
            raise HeaderFormatError(
                "Can't read %d bytes, read %d bytes instead" % (
                    header_size, len(header) + 1))

        self.header_chunk = header = "%c%s" % (header_size, header)
        self._header.read(header)

        if not self._header.valid:
            raise HeaderFormatError("Not FIT filetype")

        if self._header.total_size != self.file_size:
            raise HeaderFormatError(
                "File size should be %d bytes, but actually is %d bytes" % (
                    self._header.total_size, self.file_size))

        return self._header

    @property
    def body(self):
        if not self._body:
            self._fd.seek(self.header.size)

            body = self._fd.read(self.header.data_size)
            if len(body) != self.header.data_size:
                raise BodyFormatError(
                    "Can't read %d bytes, read %d bytes instead" % (
                        self.header.data_size, len(body)))

            header = "" if self.header.crc.value else self.header_chunk
            if not self.crc.check(header + body):
                raise BodyFormatError("Invalid CRC %x, should be %x" % (
                    compute_crc(body), self.crc.value))

            self._body.read(body)
        return self._body

    @property
    def crc(self):
        if not self._crc:
            self._fd.seek(self.header.size + self.header.data_size)

            chunk = self._fd.read(self._crc.size)
            if len(chunk) != self._crc.size:
                raise CrcFormatError(
                    "Can't read %d bytes, read %d bytes instead" % (
                        self.header.data_size, len(chunk)))

            self._crc.read(chunk)
        return self._crc
