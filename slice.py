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
    emoticonId = CEmoticon.get("id")
    EmoticonDataNormalized[emoticonId] = CEmoticon

    Image = CEmoticon.find("Image")
    if Image != None and Image.get("TextureSheet") != None and len(Image.get("TextureSheet")) > 0:
        Sheets[emoticonId] = PillowImage.open("data/sheets/%s.png" % Image.get("TextureSheet"))

EmoticonPackDataNormalized = {}
for CEmoticonPack in EmoticonPackData:
    emoticonId = CEmoticonPack.get("id")
    EmoticonPackDataNormalized[emoticonId] = CEmoticonPack

SECRET = {
    "SapperPackBonus": "Sapper Bonus"
}

for CEmoticonPack in EmoticonPackData:
    emoticonId = CEmoticonPack.get("id")
    EmoticonArrays = CEmoticonPack.findall("EmoticonArray")
    if len(EmoticonArrays) == 0: 
        print("Skipping CEmoticonPack %s" % emoticonId)
        continue
    PackName = Locale.EmoticonPack.Name[emoticonId]
    if PackName is None and emoticonId in SECRET:
        PackName = SECRET[emoticonId]

    CategoryName = None
    if CEmoticonPack.find("CollectionCategory") is not None:
        CategoryName = Locale.CollectionCategory.Name[CEmoticonPack.find("CollectionCategory").get("value")]
    else:
        if CEmoticonPack.get("parent") not in EmoticonPackDataNormalized:
            print("Skipping CEmoticonPack %s" % emoticonId)
            continue
        Parent = EmoticonPackDataNormalized[CEmoticonPack.get("parent")]
        CategoryName = "%s/%s" % (Locale.CollectionCategory.Name[Parent.find("CollectionCategory").get("value")], Parent.find("EventName").get("value"))
    for EmoticonArray in EmoticonArrays:
        Emoticon = EmoticonDataNormalized[EmoticonArray.get("value")]
        Sheet = None
        if Emoticon.get("id") not in Sheets:
            if Emoticon.get("parent") not in Sheets:
                print("Missing sheet for %s!" % EmoticonArray.get("value"))
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
