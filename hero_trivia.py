# encoding: utf-8
from Storm.Localized import Strings as LocalizedStrings
from Storm.GameData import Catalog
from sys import argv, stderr
from os.path import exists

def print_utf8(text):
    print(text)

def print_utf8_e(text):
    print(text, file=stderr)

if __name__ != '__main__':
    print_utf8_e('herotrivia.py is a CLI file, not a module')
    exit(-1)

if len(argv) < 2:
    print_utf8_e('Usage: python %s path_to_mods_dir [locale]' % (argv[0]))
    exit(1)

RootDir = argv[1]
RootDirLength = len(RootDir)

RootLocale = 'enus'
if len(argv) > 2:
    RootLocale = argv[2]

GameDataList = ['%s/heroesdata.stormmod' % RootDir]
GameDataList += list(map(lambda x: '%s/%s/' % (RootDir, x.get('value').lower()[5:]), Catalog('%s/heroesdata.stormmod/base.stormdata/Includes.xml' % RootDir)))
print('Name, Radius, Inner Radius, Flags')
for gameDataDir in GameDataList:
    gameDataPath = '%s/base.stormdata/GameData.xml' % gameDataDir
    if not exists(gameDataPath):
        print_utf8_e('Catalog stormmod %s does not exist!' % gameDataPath)
        continue
    CLocale = LocalizedStrings({}).Load('%s/%s.stormdata/LocalizedData/GameStrings.txt' % (gameDataDir, RootLocale))
    GameDataCatalog = set(map(lambda x: x.get('path'), Catalog(gameDataPath).findall("Catalog")))
    for CatalogEntry in GameDataCatalog:
        catalogPath = '%s/base.stormdata/%s' % (gameDataDir, CatalogEntry)
        if not exists(catalogPath):
            print_utf8_e('Catalog file %s does not exist!' % catalogPath)
            continue
        CatalogFile = Catalog(catalogPath)
        for CUnit in CatalogFile.findall('CUnit'):
            CUnitId = CUnit.get('id')
            CUnitParent = CUnit.get('parent') or CUnitId
            if CUnitParent.startswith('StormHero') is not True and CUnitId != 'RexxarMisha': continue
            
            CUnitName = CLocale.get("Unit/Name/%s" % CUnitId)
            CUnitRadius = 'Inherited'
            if CUnit.find('Radius') is not None: CUnitRadius = CUnit.find('Radius').get('value')
            CUnitInnerRadius = 'Inherited'
            if CUnit.find('InnerRadius') is not None: CUnitInnerRadius = CUnit.find('InnerRadius').get('value')
            CUnitFlags = list(map(lambda x: x.get('index'), filter(lambda x: x.get('value') == '1', CUnit.findall('HeroPlaystyleFlags'))))
            CUnitFlags += list(filter(lambda x: x is not None and (x.startswith('HeroGeneric') or x == 'UltimateEvolutionInvalidTarget'), map(lambda x: x.get('Link'), CUnit.findall('BehaviorArray'))))
            if len(CUnitFlags) == 0: CUnitFlags = ['Inherited']
            print('%s, %s, %s, %s' % (CUnitName, CUnitRadius, CUnitInnerRadius, ', '.join(CUnitFlags)))
