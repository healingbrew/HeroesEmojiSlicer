from PIL import Image as PillowImage
from Storm.Localized import Strings as LocalizedStrings
from Storm.GameData import Catalog, IsHidden
from os import makedirs
from os.path import exists, normpath
from math import floor, ceil
from subprocess import call as CallProcess
from sys import argv

def print_utf8(text):
    print(text.encode('utf-8'))

if __name__ != '__main__':
    print_utf8('extract_emoji.py is a CLI file, not a module')
    exit(-1)

if len(argv) < 2:
    print_utf8('Usage: python %s path_to_mods_dir [locale]' % (argv[0]))
    exit(1)

RootDir = argv[1]
RootLocale = 'enus'
if len(argv) > 2:
    RootLocale = argv[2]
Locale = LocalizedStrings({}).Load('%s/heroesdata.stormmod/%s.stormdata/LocalizedData/GameStrings.txt' % (RootDir, RootLocale))
EmoticonData = Catalog('%s/heroesdata.stormmod/base.stormdata/GameData/EmoticonData.xml' % RootDir)
EmoticonPackData = Catalog('%s/heroesdata.stormmod/base.stormdata/GameData/EmoticonPackData.xml' % RootDir)
TextureSheetData = Catalog('%s/heroesdata.stormmod/base.stormdata/GameData/TextureSheetData.xml' % RootDir)

EmoticonDataNormalized = {}
EmoticonPackDataNormalized = {}
Sheets = {}
SheetsActual = {}
TextureSheets = {}
ProcessedEmoji = []

TempPath = 'tmp/emoji'

if not exists(TempPath): makedirs(TempPath)

for CTextureSheet in TextureSheetData:
    TextureSheetId = CTextureSheet.get('id')
    TextureSheets[TextureSheetId] = CTextureSheet

for CEmoticon in EmoticonData:
    emoticonId = CEmoticon.get('id')
    EmoticonDataNormalized[emoticonId] = CEmoticon

    Images = CEmoticon.findall('Image')
    if len(Images) == 0:
        continue
    Image = Images[-1]
    if Image.get('TextureSheet') != None and len(Image.get('TextureSheet')) > 0:
        TextureSheet = Image.get('TextureSheet')
        Sheets[emoticonId] = TextureSheet
        if TextureSheet in SheetsActual or TextureSheet not in TextureSheets:
            continue
        CTextureSheet = TextureSheets[TextureSheet]
        CTextureSheetPath = CTextureSheet.findall('Image')[-1].get('value')
        CTextureSheetRows = int(CTextureSheet.findall('Rows')[-1].get('value'))
        CTextureSheetColumns = int(CTextureSheet.findall('Columns')[-1].get('value'))
        TextureSheetPath = normpath('%s/heroes.stormmod/base.stormassets/%s' % (RootDir, CTextureSheetPath.replace('\\', '/')))
        if not exists(TextureSheetPath):
            print_utf8('Can\'t find %s!' % TextureSheetPath)
            continue
        print_utf8('Converting %s' % TextureSheet)
        CallProcess(['convert', TextureSheetPath, '-format', 'png', '%s/%s.png' % (TempPath, TextureSheet)], shell=False)
        SheetsActual[TextureSheet] = (PillowImage.open('%s/%s.png' % (TempPath, TextureSheet)), CTextureSheetRows, CTextureSheetColumns)

for CEmoticonPack in EmoticonPackData:
    emoticonId = CEmoticonPack.get('id')
    EmoticonPackDataNormalized[emoticonId] = CEmoticonPack

SECRET = {
    'SapperPackBonus': 'Sapper Bonus'
}

def extract_emoji(Image, SheetData, PackName, CategoryName, EmoticonName, Scale = 1):
    if Scale == 1:
        if len(CategoryName) > 0:
            print_utf8('%s (%s) %s' % (PackName, CategoryName, EmoticonName))
        else:
            print_utf8('%s %s' % (PackName, EmoticonName))
    Base = 'emoji'
    if Scale > 1:
        Base = 'emoji-%dx' % (Scale)
    elif Scale < 1:
        Scale = 1
    Sheet, Rows, Columns = SheetData
    SlicedEmojiPath = '%s/%s/%s' % (Base, CategoryName, PackName)
    if not exists(SlicedEmojiPath): makedirs(SlicedEmojiPath)
    SlicedEmojiFilename = '%s/%s' % (SlicedEmojiPath, EmoticonName[1:-1])
    ActualWidth = Sheet.width / Columns
    ActualHeight = Sheet.height / Rows
    Width = int(Image.get('Width') or ActualWidth)
    Height = int(Image.get('Height') or ActualHeight)
        
    if Image.get('DurationPerFrame') is not None:
        Delay = float(Image.get('DurationPerFrame') or '150.0') / 600.0
        Count = int(Image.get('Count') or 1)
        Frames = ['convert', '-delay', str(Delay), '-loop', str(0), '-dispose', 'Background']
        for Index in range(0, Count):
            X = (Index % Columns) * ActualWidth
            Y = int(floor(Index / Columns) * ActualHeight)
            Box = (X, Y, X + Width, Y + Height)
            Frame = Sheet.crop(Box)
            if not Frame.getbbox(): continue
            if not exists('%s_frames' % SlicedEmojiFilename): makedirs('%s_frames' % SlicedEmojiFilename)
            if Scale != 1:
                Frame = Frame.resize((Width * Scale, Height * Scale), PillowImage.NEAREST)
            Frame.save('%s_frames/%d.png' % (SlicedEmojiFilename, Index))
            Frames.append('%s_frames/%d.png' % (SlicedEmojiFilename, Index))
        Frames.append('%s.gif' % SlicedEmojiFilename)
        CallProcess(Frames, shell=False)
    else:
        Index = int(Image.get('Index') or '0')
        X = (Index % Columns) * ActualWidth
        Y = int(floor(Index / Columns) * ActualHeight)
        Box = (X, Y, X + Width, Y + Height)
        EmojiCrop = Sheet.crop(Box)
        if Scale != 1:
            EmojiCrop = EmojiCrop.resize((Width * Scale, Height * Scale), PillowImage.NEAREST)
        EmojiCrop.save('%s.png' % SlicedEmojiFilename)

def prepare_emoji(PackName, CategoryName, EmoticonName, EmoticonId, Emoticon):
    Sheet = None
    if Emoticon.get('id') not in Sheets:
        if Emoticon.get('parent') not in Sheets:
            print_utf8('Missing sheet for %s!' % EmoticonId)
            return
        else:
            Sheet = SheetsActual[Sheets[Emoticon.get('parent')]]
    else:
        Sheet = SheetsActual[Sheets[Emoticon.get('id')]]

    Image = Emoticon.findall('Image')[-1]
    extract_emoji(Image, Sheet, PackName, CategoryName, EmoticonName, 2)
    extract_emoji(Image, Sheet, PackName, CategoryName, EmoticonName)

for CEmoticonPack in EmoticonPackData:
    EmoticonPackId = CEmoticonPack.get('id')
    EmoticonArrays = CEmoticonPack.findall('EmoticonArray')
    if len(EmoticonArrays) == 0: 
        print_utf8('Skipping CEmoticonPack %s' % EmoticonPackId)
        continue
    PackName = Locale.EmoticonPack.Name[EmoticonPackId]
    if PackName is None:
        if EmoticonPackId in SECRET:
            PackName = SECRET[EmoticonPackId]
        elif CEmoticonPack.find('Name') is not None:
            PackName = Locale.get(CEmoticonPack.findall('Name')[-1].get('value'))
        else:
            PackName = EmoticonPackId

    CategoryName = None
    if CEmoticonPack.find('CollectionCategory') is not None:
        CategoryName = Locale.CollectionCategory.Name[CEmoticonPack.findall('CollectionCategory')[-1].get('value')]
    else:
        if CEmoticonPack.get('parent') not in EmoticonPackDataNormalized:
            print_utf8('Skipping CEmoticonPack %s' % EmoticonPackId)
            continue
        Parent = EmoticonPackDataNormalized[CEmoticonPack.get('parent')]
        CategoryName = '%s/%s' % (Locale.CollectionCategory.Name[Parent.findall('CollectionCategory')[-1].get('value')], Parent.findall('EventName')[-1].get('value'))
    for EmoticonArray in EmoticonArrays:
        EmoticonId = EmoticonArray.get('value')
        Emoticon = EmoticonDataNormalized[EmoticonId]
        ProcessedEmoji.append(EmoticonId)
        EmoticonName = Locale.Emoticon.Name[EmoticonId]
        if EmoticonName is None:
            if EmoticonArray.find('Name') is not None:
                EmoticonName = Locale.get(EmoticonArray.findall('Name')[-1].get('value'))
            else:
                EmoticonName = ':%s:' % EmoticonId 
        prepare_emoji(PackName, CategoryName, EmoticonName, EmoticonId, Emoticon)

for EmoticonId in EmoticonDataNormalized.keys():
    if EmoticonId not in ProcessedEmoji:
        Emoticon = EmoticonDataNormalized[EmoticonId]
        if int(Emoticon.get('default') or '0') == 1 or Emoticon.get('parent') == 'abstract_emoticon':
            print_utf8('Skipping CEmoticon %s' % EmoticonId)
            continue
        EmoticonName = Locale.Emoticon.Name[EmoticonId]
        if EmoticonName is None:
            if EmoticonArray.find('Name') is not None:
                EmoticonName = Locale.get(Emoticon.findall('Name')[-1].get('value'))
            else:
                EmoticonName = ':%s:' % EmoticonId 
        prepare_emoji('Uncategorized', '', EmoticonName, EmoticonId, Emoticon)
