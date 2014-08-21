from struct import Struct

from fit.exceptions import BodyFormatError
from fit.structure.crc import Crc, compute_crc


class Header(object):
    def __init__(self):
        self._format = Struct("<BBHL4s")

        self.size = None

        self.data_type = ".FIT"
        self.data_size = None

        self.crc = Crc()

        self.protocol_version = 16
        self.profile_version = 1005

    def __nonzero__(self):
        return self.size is not None

    def __repr__(self):
        return '<%s protocol=%d profile=%d crc=%r>' % (
            self.__class__.__name__,
            self.protocol_version,
            self.profile_version,
            self.crc
        )

    @property
    def total_size(self):
        return self.size + self.data_size + self.crc.size

    @property
    def valid(self):
        return self.data_type == ".FIT"

    def read(self, chunk):
        (
            self.size, self.protocol_version, self.profile_version,
            self.data_size, self.data_type
        ) = self._format.unpack(chunk[:12])

        if len(chunk) == 14:
            self.crc.read(chunk[12:])

            if self.crc.value and not self.crc.check(chunk[:12]):
                raise BodyFormatError("Invalid CRC %x, should be %x" % (
                    compute_crc(chunk[:12]), self.crc.value))

    def write(self):
        self.size = 14
        chunk = self._format.pack(self.size, self.protocol_version,
                                  self.profile_version, self.data_size,
                                  self.data_type)
        self.crc.value = compute_crc(chunk)
        return chunk + self.crc.write()
