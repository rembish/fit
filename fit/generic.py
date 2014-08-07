from contextlib import closing
from io import BytesIO, FileIO
from os import fstat
from struct import pack, unpack, Struct


#from fit.helper import Header
#from fit.record import Record, DefinitionRecord








class Data(object):
    def __init__(self):
        self._buffer = None
        self._records = None

    def __nonzero__(self):
        return self._records is not None

    def read(self, buffer):
        self._buffer = buffer
        self._records = []





if __name__ == '__main__':
    fd = open("../2014-07-10-17-08-11.fit", "rb")
    reader = Reader(fd)
    print reader.body
    #ff = open()
    #print len(ff.body.getvalue())
