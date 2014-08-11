from fit.reader import Reader

if __name__ == '__main__':
    fd = open("../2014-07-10-17-08-11.fit", "rb")
    reader = Reader(fd)
    print reader.body
