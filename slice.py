from PIL import Image as PillowImage
from Storm.Localized import Strings as LocalizedStrings
from Storm.GameData import Catalog, IsHidden
from os import makedirs
from os.path import exists
from math import floor
from subprocess import call as CallProcess
from sys import argv

def print_utf8(text):
    print(text.encode('utf-8'))

if __name__ != '__main__':
    print_utf8('slice.py is a CLI file, not a module')
    exit(-1)

if len(argv) < 2:
    print_utf8('Usage: python %s path_to_mods_parent_dir [locale]' % (argv[0]))
    exit(1)

RootDir = argv[1]
RootLocale = 'enus'
if len(argv) > 2:
    RootLocale = argv[2]

Locale = LocalizedStrings({}).Load('%s/mods/heroesdata.stormmod/%s.stormdata/LocalizedData/GameStrings.txt' % (RootDir, RootLocale))
EmoticonData = Catalog('%s/mods/heroesdata.stormmod/base.stormdata/GameData/EmoticonData.xml' % RootDir)
EmoticonPackData = Catalog('%s/mods/heroesdata.stormmod/base.stormdata/GameData/EmoticonPackData.xml' % RootDir)

EmoticonDataNormalized = {}
Sheets = {}

TempPath = 'tmp/emoji'

if not exists(TempPath): makedirs(TempPath)

for CEmoticon in EmoticonData:
    emoticonId = CEmoticon.get('id')
    EmoticonDataNormalized[emoticonId] = CEmoticon

    Image = CEmoticon.find('Image')
    if Image != None and Image.get('TextureSheet') != None and len(Image.get('TextureSheet')) > 0:
        TextureSheet = Image.get('TextureSheet')
        TextureSheetPath = '%s/mods/heroes.stormmod/base.stormassets/Assets/Textures/%s.dds' % (RootDir, TextureSheet)
        if not exists(TextureSheetPath):
            print_utf8('Can\'t find %s!' % TextureSheetPath)
            continue
        CallProcess(['convert', TextureSheetPath, '-format', 'png', '%s/%s.png' % (TempPath, TextureSheet)], shell=False)
        Sheets[emoticonId] = PillowImage.open('%s/%s.png' % (TempPath, TextureSheet))

EmoticonPackDataNormalized = {}
for CEmoticonPack in EmoticonPackData:
    emoticonId = CEmoticonPack.get('id')
    EmoticonPackDataNormalized[emoticonId] = CEmoticonPack

SECRET = {
    'SapperPackBonus': 'Sapper Bonus'
}

for CEmoticonPack in EmoticonPackData:
    emoticonId = CEmoticonPack.get('id')
    EmoticonArrays = CEmoticonPack.findall('EmoticonArray')
    if len(EmoticonArrays) == 0: 
        print_utf8('Skipping CEmoticonPack %s' % emoticonId)
        continue
    PackName = Locale.EmoticonPack.Name[emoticonId]
    if PackName is None and emoticonId in SECRET:
        PackName = SECRET[emoticonId]

    CategoryName = None
    if CEmoticonPack.find('CollectionCategory') is not None:
        CategoryName = Locale.CollectionCategory.Name[CEmoticonPack.find('CollectionCategory').get('value')]
    else:
        if CEmoticonPack.get('parent') not in EmoticonPackDataNormalized:
            print_utf8('Skipping CEmoticonPack %s' % emoticonId)
            continue
        Parent = EmoticonPackDataNormalized[CEmoticonPack.get('parent')]
        CategoryName = '%s/%s' % (Locale.CollectionCategory.Name[Parent.find('CollectionCategory').get('value')], Parent.find('EventName').get('value'))
    for EmoticonArray in EmoticonArrays:
        Emoticon = EmoticonDataNormalized[EmoticonArray.get('value')]
        Sheet = None
        if Emoticon.get('id') not in Sheets:
            if Emoticon.get('parent') not in Sheets:
                print_utf8('Missing sheet for %s!' % EmoticonArray.get('value'))
                continue
            else:
                Sheet = Sheets[Emoticon.get('parent')]
        else:
            Sheet = Sheets[Emoticon.get('id')]

        Image = Emoticon.find('Image')
    
        EmoticonName = Locale.Emoticon.Name[EmoticonArray.get('value')]
        print_utf8('%s (%s) %s' % (PackName, CategoryName, EmoticonName))
        SlicedEmojiPath = 'emoji/%s/%s' % (CategoryName, PackName)
        if not exists(SlicedEmojiPath): makedirs(SlicedEmojiPath)
        SlicedEmojiFilename = '%s/%s' % (SlicedEmojiPath, EmoticonName[1:-1])
        Width = int(Image.get('Width'))
        Height = 32
            
        if Image.get('DurationPerFrame') is not None:
            Delay = float(Image.get('DurationPerFrame') or '150.0') / 600.0
            Count = int(Image.get('Count') or 1)
            Frames = ['convert', '-delay', str(Delay), '-loop', str(0), '-dispose', 'Background']
            for Index in range(0, Count):
                X = (Index % 4) * 40
                Y = int(floor(Index / 4) * 32)
                Box = (X, Y, X + Width, Y + Height)
                Frame = Sheet.crop(Box)
                if not exists('%s_frames' % SlicedEmojiFilename): makedirs('%s_frames' % SlicedEmojiFilename)
                Frame.save('%s_frames/%d.png' % (SlicedEmojiFilename, Index))
                Frames.append('%s_frames/%d.png' % (SlicedEmojiFilename, Index))
            Frames.append('%s.gif' % SlicedEmojiFilename)
            CallProcess(Frames, shell=False)
        else:
            Index = int(Image.get('Index') or '0')
            X = (Index % 4) * 40
            Y = int(floor(Index / 4) * 32)
            Box = (X, Y, X + Width, Y + Height)
            Sheet.crop(Box).save('%s.png' % SlicedEmojiFilename)
