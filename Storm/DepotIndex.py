from struct import unpack_from, calcsize
from os import stat

class DepotIndexRecord(object):

    def __init__(self, size, u1, u2, u3, fileType, path, root):
        self.size = size
        self.type = fileType
        self.path = '%sCache%s' % (root, path.replace('\\', '/'))
        self.time = stat(self.path).st_mtime

    def __str__(self): return self.path


class DepotIndex(object):

    def __init__(self, depotPath):
        self.root = depotPath
        with open('%s/index' % (self.root), 'rb') as depot:
            depot.seek(0, 2)
            eos = depot.tell()
            depot.seek(0, 0)
            version = unpack_from('<I', depot.read(4))[0]
            self.types = {}
            fmt = '<IIII4s'
            fmtSize = calcsize(fmt)
            while depot.tell() != eos:
                block = unpack_from(fmt, depot.read(fmtSize))
                text = []
                while True:
                    ch = depot.read(1).decode('ascii')
                    if ch == b'\x00' or ch == chr(0):
                        break
                    text.append(str(ch))
                record = DepotIndexRecord(block[0], block[1], block[2], block[3], str(block[4][::-1].decode('ascii').replace('\0', '')), ''.join(text), self.root)
                if record.type not in self.types:
                    self.types[record.type] = []
                self.types[record.type].append(record)
                depot.read(block[4].decode('ascii').count('\0'))

    def __getattr__(self, key):
        return self[key]

    def __getitem__(self, key):
        if type(key) is slice:
            return self.types[key.start:key.stop:key.step]
        if key in self.types:
            return self.types[key]
