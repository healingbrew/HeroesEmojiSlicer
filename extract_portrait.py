from Storm.DepotIndex import DepotIndex
from Storm.DepotLdptFile import DepotLdptFile
from sys import argv
from os.path import exists

def print_utf8(text):
    print(text.encode('utf-8'))

if __name__ != '__main__':
    print_utf8('extract_portrait.py is a CLI file, not a module')
    exit(-1)

if len(argv) < 2:
    print_utf8('Usage: python %s path_to_mods_dir [path_to_program_data [locale [region]]]' % (argv[0]))
    exit(1)

RootDir = argv[1]
RootDirLength = len(RootDir)

RootDepotDir = 'C:/ProgramData/Blizzard Entertainment/Battle.net/' 
if len(argv) > 2:
    RootDepotDir = argv[2]
RootDepotDirLength = len(RootDepotDir)

RootLocale = 'enus'
if len(argv) > 3:
    RootLocale = argv[3]

# 1 = us, 2 = eu, 3 = ko, 5? = cn, 98 = xx (ww ptr), ?? = cxx (cn ptr), ?? = xx-02 (tournament)
RootRegion = 1
if len(argv) > 4:
    RootRegion = int(argv[4])

print_utf8('Loading portrait data')
Depot = DepotIndex(RootDepotDir)
Ldpt = DepotLdptFile(list(filter(lambda x: exists(x), map(lambda x: x.path, sorted(Depot.ldpt, key=lambda x: x.time, reverse=True))))[0], RootDepotDir)
print(Ldpt.data)
