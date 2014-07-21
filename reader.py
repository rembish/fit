from hexdump import hexdump
from os import stat, SEEK_END
from struct import unpack

from fit.constants import MESSAGE_NUMBERS

def get_byte(fp):
    return ord(fp.read(1))


def fit_crc(crc, byte):
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


class Field(object):
    _types = ["enum", "sint8", "uint8", "sint16", "uint16", "sint32", "uint32",
              "string", "float32", "float64", "uint8z", "uint16z", "uint32z",
              "byte"]

    def __init__(self, chunk):
        self.definition = ord(chunk[0])
        self.size = ord(chunk[1])
        self.base_type = ord(chunk[2])
        self.base_type_number = self.base_type & 0b00011111

    @property
    def type(self):
        return self._types[self.base_type_number]


class Fields(list):
    def __init__(self, chunk):
        super(Fields, self).__init__()

        field_size = 3
        for offset in range(0, len(chunk), field_size):
            self.append(Field(chunk[offset:offset + field_size]))

    @property
    def size(self):
        return sum(map(lambda x: x.size, self))


filename = "2014-07-12-12-48-15.fit"
filesize = stat(filename).st_size
print 'Filesize: %d' % filesize


fp = open(filename, 'rb')

header_size = get_byte(fp)
print "Header size: %d" % header_size

header = fp.read(header_size - 1)

hexdump(header)

protocol_version, profile_version, data_size, data_type, crc = \
    unpack("<BHL4sH", header)
crc_size = 2

assert data_type == '.FIT'
assert data_size + header_size + crc_size == filesize

message_types = {}

# ...
while fp.tell() != filesize - crc_size:
    position = fp.tell()
    record_header = ord(fp.read(1))

    record_type = record_header & (1 << 7)
    if not record_type:
        print "[%d] Normal header" % position
        message_type = record_header & (1 << 6)
        local_message_type = record_header & 0b00001111

        if message_type:
            print "[%d] Definition Message of type #%d" % (
                position, local_message_type)
            reserved, architecture = unpack("<BB", fp.read(2))

            assert reserved == 0

            architecture = ">" if architecture else "<"
            global_message_number, number_of_fields = \
                unpack("%sHB" % architecture, fp.read(3))

            print "[%d] Global message number #%d: %s" % (
                position, global_message_number,
                MESSAGE_NUMBERS.get(global_message_number, "???"))
            print "[%d] Number of fields: %d" % (
                position, number_of_fields)

            field_size = 3
            fields_data = fp.read(field_size * number_of_fields)
            hexdump(fields_data)

            message_types[local_message_type] = Fields(fields_data)
        else:
            print "[%d] Data Message of type #%d" % (
                position, local_message_type)
            message_size = message_types[local_message_type].size
            print "[%d] Message size: %d" % (fp.tell() - 1, message_size)

            message_data = fp.read(message_size)
            hexdump(message_data)

            current = 0
            for field in message_types[local_message_type]:
                print "[%d] %s field[%d] with value %s" % (
                    position, field.type, field.definition,
                    hexdump(message_data[current:current + field.size], "return")
                )
                current += field.size

    else:
        print "[%d] Compressed timestamp header" % position
        local_message_type = record_header & 0b01100000
        time_offset = record_header & 0b00011111

fp.seek(-crc_size, SEEK_END)
ending_crc = unpack("<H", fp.read(crc_size))[0]

print "Front CRC: %d\nEnd CRC: %d" % (crc, ending_crc)
