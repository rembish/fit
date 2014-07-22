from contextlib import closing
from io import BytesIO, FileIO
from os import fstat
from struct import unpack

from fit.helper import Header
from fit.record import Record, DefinitionRecord


def open(filename, mode='rb'):
    if mode != 'rb':
        raise Exception()  # FIXME

    with closing(FileIO(filename, mode)) as fd:
        header_size = ord(fd.read(1))
        if header_size < 12:
            raise Exception()  # FIXME

        fd.seek(0)
        header = Header(fd.read(header_size))
        if not header.valid():
            raise Exception()  # FIXME

        crc_size = 2
        filesize = fstat(fd.fileno()).st_size
        if filesize != header_size + header.data_size + crc_size:
            raise Exception()  # FIXME

        body = BytesIO(fd.read(header.data_size))
        crc = unpack("<H", fd.read(crc_size))[0]
        return FitFile(body, header=header, crc=crc)


class Fit(object):
    def __init__(self, filename, mode='r'):
        self.header = Header()
        self.crc = Crc()

        self.definitions = {}
        self.records = []

        if mode not in 'arw':
            raise Exception()

        self.fd = FileIO(filename, mode='%sb' % mode)
        if self.mode in 'ra':
            self.read()

    def __getitem__(self, x):
        return self.records[x]

    def read(self):
        pass

    @property
    def mode(self):
        return self.fd.mode[0]

    @property
    def name(self):
        return self.fd.name

    @property
    def closed(self):
        return self.fd.closed


class FitFile(object):
    def __init__(self, stream, header=None, crc=None):
        self.header = header
        self.crc = crc
        self.records = {}
        self.data = []

        self.process(stream)

    def process(self, stream):
        while True:
            record = Record.open(stream.read(1))
            if not record:
                break

            if isinstance(record, DefinitionRecord):
                record.build(stream)
                self.records[record.id] = record.message

            if not record.compressed:
                record.read(stream.read(self.records[record.id].size))
                self.data.append(record)

            else:
                pass  # TODO






if __name__ == '__main__':
    ff = open("../2014-07-12-12-48-15.fit")
    print len(ff.body.getvalue())
