import json 

class DepotLdptEntry(object):
    def __init__(self, path, index, cols, rows):
        self.path = path
        self.index = index
        self.cols = cols
        self.rows = rows

class DepotLdptFile(object):

    def __init__(self, path, root):
        with open(path, 'r') as text:
            ldpt = json.loads('[' + text.readline().replace('}{', '},{') + ']')
            info = ldpt[0]
            self.data = {}
            for index in range(1, len(ldpt), 2):
                handle = ldpt[index]['m_cacheHandle'][16:]
                entry = ldpt[index + 1]
                path = "%s/%s/%s/%s.wafl" % (root, handle[0:2], handle[2:4], handle)
                self.data[entry['m_textureFileIndex']] = DepotLdptEntry(path, entry['m_textureFileIndex'], entry['m_textureCols'], entry['m_textureRows'])
