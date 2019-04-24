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
                (key, value) = line.split('=', 1)
                parts = key.split('/')
                d = self.data
                for part in parts:
                    try:
                        if part not in d:
                            if part == parts[-1]:
                                d[part] = value
                            else:
                                d[part] = {}
                        d = d[part]
                    except: break
                line = f.readline()
        return self

    def __getattr__(self, key):
        return self[key]

    def __getitem__(self, key):
        if type(key) is slice:
            return self.data[key.start:key.stop:key.step]
        if key in self.data:
            if type(self.data[key]) is str:
                return self.data[key]
            if sys.version_info[0] < 3 and type(self.data[key]) is unicode:
                return self.data[key]
            return Strings(self.data[key])

    def __str__(self): return self.data.__str__()
