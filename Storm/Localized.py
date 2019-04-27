import codecs
import sys

class Strings(object):
    
    def __init__(self, data):
        self.data = data

    def Load(self, path):
        with codecs.open(path, 'r', 'utf8') as f:
            line = f.readline()
            while len(line or '') > 0:
                line = line.strip()
                while u'\ufeff' == line[:1] or u'\uffef' == line[:1]:
                    line = line[1:]
                (key, value) = line.split('=', 1)
                parts = key.split('/')
                d = self.data
                try:
                    for partIndex in range(len(parts)):
                        part = parts[partIndex]
                        if part not in d:
                            if partIndex == len(parts) - 1:
                                d[part] = value
                            else:
                                d[part] = {}
                        d = d[part]
                except: pass
                line = f.readline()
        return self

    def get(self, key):
        parts = key.split('/')
        nextObj = self
        for part in parts:
            if nextObj == None: break
            nextObj = nextObj[part]
        return nextObj

    def __getattr__(self, key):
        return self[key]

    def __getitem__(self, key):
        if type(key) is slice:
            return self[key.start:key.stop:key.step]
        if key in self.data:
            if type(self.data[key]) is str:
                return self.data[key]
            if sys.version_info[0] < 3 and type(self.data[key]) is unicode:
                return self.data[key]
            return Strings(self.data[key])
        return None

    def __str__(self): return self.data.__str__()
