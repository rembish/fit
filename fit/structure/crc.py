from struct import Struct


def _process_byte(crc, byte):
    crc_table = [
        0x0000, 0xcc01, 0xd801, 0x1400, 0xf001, 0x3c00, 0x2800, 0xe401,
        0xa001, 0x6c00, 0x7800, 0xb401, 0x5000, 0x9c01, 0x8801, 0x4400,
    ]

    temp = crc_table[crc & 0xf]
    crc = (crc >> 4) & 0x0fff
    crc = crc ^ temp ^ crc_table[byte & 0xf]

    temp = crc_table[crc & 0xf]
    crc = (crc >> 4) & 0x0fff
    crc = crc ^ temp ^ crc_table[(byte >> 4) & 0xf]

    return crc


def compute_crc(chunk):
    crc = 0
    for i in range(len(chunk)):
        char = ord(chunk[i])
        crc = _process_byte(crc, char)
    return crc


class Crc(object):
    def __init__(self):
        self._format = Struct("<H")

        self.size = self._format.size
        self.value = None

    def __nonzero__(self):
        return self.value is not None

    def __repr__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.value or "-")

    def read(self, chunk):
        self.value = self._format.unpack(chunk)[0]

    def write(self):
        return self._format.pack(self.value or 0)

    def check(self, chunk):
        return compute_crc(chunk) == self.value
