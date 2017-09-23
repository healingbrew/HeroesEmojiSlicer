from PIL import Image as PillowImage
from Storm.Localized import Strings as LocalizedStrings
from Storm.GameData import Catalog, IsHidden
from os import makedirs
from os.path import exists
from math import floor

Locale = LocalizedStrings({}).Load("data/GameStrings.txt")
EmoticonData = Catalog("data/EmoticonData.xml")
EmoticonPackData = Catalog("data/EmoticonPackData.xml")

EmoticonDataNormalized = {}
Sheets = {}

for CEmoticon in EmoticonData:
    if IsHidden(CEmoticon): continue
    EmoticonDataNormalized[CEmoticon.get("id")] = CEmoticon

    Image = CEmoticon.find("Image")
    if Image != None and Image.get("TextureSheet") != None:
        Sheets[CEmoticon.get("id")] = PillowImage.open("data/sheets/%s.png" % Image.get("TextureSheet"))

for CEmoticonPack in EmoticonPackData:
    if IsHidden(CEmoticonPack): continue
    id = CEmoticonPack.get("id")

    PackName = Locale.EmoticonPack.Name[id]
    CategoryName = Locale.CollectionCategory.Name[CEmoticonPack.find("CollectionCategory").get("value")]
    for EmoticonArray in CEmoticonPack.findall("EmoticonArray"):
        Emoticon = EmoticonDataNormalized[EmoticonArray.get("value")]
        Sheet = None
        if Emoticon.get("id") not in Sheets:
            if Emoticon.get("parent") not in Sheets:
                print "Missing sheet for %s!" % EmoticonArray.get("value")
                continue
            else:
                Sheet = Sheets[Emoticon.get("parent")]
        else:
            Sheet = Sheets[Emoticon.get("id")]

        Image = Emoticon.find("Image")
        Index = int(Image.get("Index") or "0")
        X = (Index % 4) * 40
        Y = int(floor(Index / 4) * 32)
        Width = int(Image.get("Width"))
        Height = 32

        EmoticonName = Locale.Emoticon.Name[EmoticonArray.get("value")]
        SlicedEmojiPath = "emoji/%s/%s" % (CategoryName, PackName)
        if not exists(SlicedEmojiPath): makedirs(SlicedEmojiPath)
        SlicedEmojiFilename = "%s/%s.png" % (SlicedEmojiPath, EmoticonName[1:-1])

        Box = (X, Y, X + Width, Y + Height)
        Sheet.crop(Box).save(SlicedEmojiFilename)
