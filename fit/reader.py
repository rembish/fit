from os import fstat

from fit.crc import Crc
from fit.exceptions import HeaderFormatError, BodyFormatError, CrcFormatError
from fit.body import Body
from fit.header import Header


class Reader(object):
    def __init__(self, fd):
        self.fd = fd

        self._header = Header()
        self._body = Body()
        self._crc = Crc()

        self.file_size = fstat(self.fd.fileno()).st_size

    def __repr__(self):
        return '<%s header=%r body=%r crc=%r>' % (
            self.__class__.__name__,
            self.header, self.body, self.crc
        )

    @property
    def header(self):
        if self._header:
            return self._header

        self.fd.seek(0)

        header_size = ord(self.fd.read(1))
        if header_size not in (12, 14):
            raise HeaderFormatError(
                "Strange size: %d bytes" % header_size)

        header = self.fd.read(header_size - 1)
        if len(header) != header_size - 1:
            raise HeaderFormatError(
                "Can't read %d bytes, read %d bytes instead" % (
                    header_size, len(header) + 1))

        header = "%c%s" % (header_size, header)
        if header_size == 14:
            header += self.fd.read(2)

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
            self.fd.seek(self.header.size)

            body = self.fd.read(self.header.data_size)
            if len(body) != self.header.data_size:
                raise BodyFormatError(
                    "Can't read %d bytes, read %d bytes instead" % (
                        self.header.data_size, len(body)))

            crc = self.header.crc or self.crc
            if not crc.check(body):
                raise BodyFormatError("Invalid CRC %x, should be %x" % (
                    crc.compute_crc(body), crc.value))

            self._body.read(body)
        return self._body

    @property
    def crc(self):
        if not self._crc:
            self.fd.seek(self.header.size + self.header.data_size)

            chunk = self.fd.read(self.header.crc.size)
            if len(chunk) != self.header.crc.size:
                raise CrcFormatError(
                    "Can't read %d bytes, read %d bytes instead" % (
                        self.header.data_size, len(chunk)))

            self._crc.read(chunk)
        return self._crc
