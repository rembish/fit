from struct import unpack


class Header(object):
    def __init__(self, data):
        (
            self.protocol_version, self.profile_version,
            self.data_size, self.data_type
        ) = unpack("<BHL4s", data[:12])

        self.crc = None
        if len(data) > 12:
            self.crc = unpack("<H", data[12:])[0]

        self.size = len(data)
        self.crc_size = 2

    def valid(self):
        return self.data_type == '.FIT'
