# encoding: utf-8
from Storm.Localized import Strings as LocalizedStrings
from Storm.GameData import Catalog
from Storm.DepotIndex import DepotIndex
from Storm.DepotCataFile import DepotCataFile, TYPE_NONE, TYPE_PRODUCTS, TYPE_LICENSES
from sys import argv
from os.path import exists

def print_utf8(text):
    print(text.encode('utf-8'))

if __name__ != '__main__':
    print_utf8('catalog.py is a CLI file, not a module')
    exit(-1)

if len(argv) < 2:
    print_utf8('Usage: python %s path_to_mods_dir [path_to_program_data [locale [region]]]' % (argv[0]))
    exit(1)

MissingProducts = []
MissingLicenses = []

def printProduct(Product, Region):
    print_utf8('\t\tName: %s' % Product["m_name"])
    print_utf8('\t\tLife Cycle: %s' % Product["m_lifeCycle"])
    print_utf8('\t\tFlags: %s' % Product["m_flags"])
    print_utf8('\t\tVisible: %s' % Product["m_visible"])
    print_utf8('\t\tRegion Visibility: %s' % next((p['m_visible'] for p in Product["m_regionalSettings"] if p['m_region'] == Region), False))
    XHS = next((p for p in Product["m_prices"] if p['m_currency'] == 'XHS' and p['m_priceType'] == 'RETAIL_VALUE'), None)
    if XHS != None:
        print_utf8('\t\tShard Cost: %s' % (XHS['m_price'] / 10000))
    XHG = next((p for p in Product["m_prices"] if p['m_currency'] == 'XHG' and p['m_priceType'] == 'RETAIL_VALUE'), None)
    if XHG != None:
        print_utf8('\t\tGold Cost: %s' % (XHG['m_price'] / 10000))
    XHC = next((p for p in Product["m_prices"] if p['m_currency'] == 'XHC' and p['m_priceType'] == 'RETAIL_VALUE'), None)
    if XHC != None:
        print_utf8('\t\tGem Cost: %s' % (XHC['m_price'] / 10000))

def parseRewards(CEntries, Region, Economy, Locale, CatalogTree, RewardEntries):
    global MissingProducts, MissingLicenses
    for CEntry in CEntries:
        RequiredRewardArray = set(map(lambda x: x.get('value'), CEntry.findall('RequiredRewardArray')))
        CType = CEntry.tag[1:]
        CId = CEntry.get('id')
        RequiredRewardArray.add(CId)
        
        try:
            CName = Locale.get('%s/Name/%s' % (CType, CId))
        except:
            CName = CId

        print_utf8('%s (%s)' % (CName, CId))
        print_utf8('\tType: %s' % CType)

        CInfoText = CEntry.find('InfoText')
        if CInfoText != None:
            print_utf8('\tInfo: %s' % Locale.get(CInfoText.get('value')))

        CSortName = CEntry.find('SortName')
        SortName = ''
        if CSortName != None:
            SortName = Locale.get(CSortName.get('value'))
            print_utf8('\tSort Name: %s' % SortName)
        
        CRarity = CEntry.find('Rarity')
        if CRarity == None:
            CRarity = 'Common'
        else:
            CRarity = CRarity.get('value')
        print_utf8('\tRarity: %s' % CRarity)
        
        CReleaseDate = CEntry.find('ReleaseDate')
        if CReleaseDate != None:
            print_utf8('\tRelease Date: %s/%s/%s' % (CReleaseDate.get('Year'), CReleaseDate.get('Month'), CReleaseDate.get('Year')))
        
        CUniverse = CEntry.find('Universe')
        if CUniverse != None:
            print_utf8('\tUniverse: %s' % CUniverse.get('value'))
        
        CCollectionCategory = CEntry.find('CollectionCategory')
        if CCollectionCategory != None:
            print_utf8('\tCategory: %s' % CCollectionCategory.get('value'))
        
        CHyperlinkId = CEntry.find('HyperlinkId')
        CHyperlink = ''
        if CHyperlinkId != None:
            CHyperlink = 'battlenet://heroes/%s/%s/%s' % (CType.lower(), Region, CHyperlinkId.get('value'))
            print_utf8('\tHyperlink: %s' % CHyperlink)
        
        CEventName = CEntry.find('EventName')
        if CEventName != None:
            print_utf8('\tEvent: %s' % CEventName.get('value'))
        
        CProductId = CEntry.find('ProductId')
        if CProductId != None:
            CProductId = CProductId.get('value')

        LicenseIds = []

        for RequiredReward in RequiredRewardArray:
            if not RequiredReward in RewardEntries:
                continue
            LicenseIds += list(map(lambda x: x.get('value'), RewardEntries[RequiredReward].findall("License")))

        Done = False

        for EconomyCatalog in Economy:
            if EconomyCatalog.type & TYPE_PRODUCTS == TYPE_PRODUCTS:
                if CProductId != None:
                    EconomyProduct = EconomyCatalog.findProducts(int(CProductId))
                    if EconomyProduct != None:
                        CProductId = None
                        if not Done:
                            Done = True
                            print_utf8('\tProduct Info:')
                            printProduct(EconomyProduct, Region)
                NewLicenseIds = []
                for LicenseId in LicenseIds:
                    EconomyLicenses = EconomyCatalog.findLicenses(int(LicenseId))
                    if EconomyLicenses == None:
                        NewLicenseIds.append(LicenseId)
                    else:
                        for EconomyLicense in EconomyLicenses:
                            print_utf8('\tBundle Info:')
                            printProduct(EconomyLicense, Region)
                LicenseIds = NewLicenseIds

        if CType == 'VoiceLine': continue

        if CProductId != None:
            MissingProducts.append('%s (%s) %s %s' % (CName, CId, CHyperlink, SortName))

        if len(LicenseIds) > 0:
            MissingLicenses.append('%s (%s) %s %s' % (CName, CId, CHyperlink, SortName))

RootDir = argv[1]
RootDirLength = len(RootDir)

RootDepotDir = 'C:/ProgramData' 
if len(argv) > 2:
    RootDepotDir = argv[2]
RootDepotDir = '%s/Blizzard Entertainment/Battle.net/' % (argv[2])
RootDepotDirLength = len(RootDepotDir)

RootLocale = 'enus'
if len(argv) > 3:
    RootLocale = argv[3]

# 1 = us, 2 = eu, 3 = ko, 5? = cn, 98 = xx (ww ptr), ?? = cxx (cn ptr), ?? = xx-02 (tournament)
RootRegion = 1
if len(argv) > 4:
    RootRegion = int(argv[4])

print_utf8('Loading economy data')
Depot = DepotIndex(RootDepotDir)
EconomyCatalogs = list(map(lambda x: DepotCataFile(x.path), Depot.cata))

GameDataList = ['%s/heroesdata.stormmod' % RootDir]
GameDataList += list(map(lambda x: '%s/%s/' % (RootDir, x.get('value').lower()[5:]), Catalog('%s/heroesdata.stormmod/base.stormdata/Includes.xml' % RootDir)))

CRewardById = {}
CCatalogs = []
CCombinedLocale = {}

print_utf8('Loading reward data')
for gameDataDir in GameDataList:
    gameDataPath = '%s/base.stormdata/GameData.xml' % gameDataDir
    if not exists(gameDataPath):
        print_utf8('Catalog stormmod %s does not exist!' % gameDataPath[RootDirLength:])
        continue
    CCombinedLocale = LocalizedStrings(CCombinedLocale).Load('%s/%s.stormdata/LocalizedData/GameStrings.txt' % (gameDataDir, RootLocale)).data
    GameDataCatalog = Catalog(gameDataPath)
    for CatalogEntry in GameDataCatalog:
        catalogPath = '%s/base.stormdata/%s' % (gameDataDir, CatalogEntry)
        if not exists(catalogPath):
            print_utf8('Catalog file %s does not exist!' % catalogPath[RootDirLength:])
            continue
        CatalogFile = Catalog(catalogPath)
        CCatalogs.append(CatalogFile)
        for CRewardType in ['Banner', 'VoiceLine', 'Spray', 'Hero', 'Skin', 'Mount', 'AnnouncerPack', 'Icon']:
            CRewards = CatalogFile.findall('CReward%s' % CRewardType)
            for CReward in CRewards: CRewardById[CReward.get('id')] = CReward

CCombinedLocale = LocalizedStrings(CCombinedLocale)

print_utf8('Parsing reward data')
for CatalogFile in CCatalogs:
    CItems = []
    for CRewardType in ['Banner', 'VoiceLine', 'Spray', 'Hero', 'Skin', 'Mount', 'AnnouncerPack', 'Icon']:
        CItems += CatalogFile.findall('C%s' % CRewardType)
    parseRewards(CItems, RootRegion, EconomyCatalogs, CCombinedLocale, CatalogFile, CRewardById)

print_utf8("Missing Products: \n\t%s" % '\n\t'.join(MissingProducts))
print_utf8("Missing Licenses: \n\t%s" % '\n\t'.join(MissingLicenses))
