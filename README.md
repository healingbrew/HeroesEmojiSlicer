# HeroesToolkit

Series of tools for parsing Heroes of the Storm files into human-friendly data.

## HeroesEmojiSlicer

Slice and Dice ![:orphcool:](https://i.imgur.com/3OmnEDg.png)

A tool for slicing emoji sprite sheets and reconstructing animated emoji.

### Installation

- Python 3.6+
- `pip3 install Pillow`
- ImageMagick (for conversion)

### Extract

- `mods/heroesdata.stormmod/base.stormdata/GameData/EmoticonPackData.xml`
- `mods/heroesdata.stormmod/base.stormdata/GameData/EmoticonData.xml`
- `mods/heroesdata.stormmod/enus.stormdata/LocalizedData/GameStrings.txt`
- `mods/heroes.stormmod/base.stormassets/Assets/Textures/storm_emoji_*.dds`

### Usage

`python slice.py path_to_mods enus`

Images will be in the "emoji" folder.

## MissingSkinFinder

Who'se that variation?! ![:orphoops:](https://i.imgur.com/hFl088z.png)

Parses catalog data to search for missing/unobtainable rewards.

### Usage

`python catalog.py path_to_mods path_to_programdata_blizzardent enus`
