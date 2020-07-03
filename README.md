# HeroesToolkit

Series of tools for parsing Heroes of the Storm files into human-friendly data.

## HeroesEmojiSlicer ![:orphcool:](https://i.imgur.com/3OmnEDg.png)

Slice and Dice.

A tool for slicing emoji sprite sheets and reconstructing animated emoji.

### Installation

- Python 3.6+
- `pip3 install Pillow mpyq`
- ImageMagick (for conversion)

### Extract

- `mods/heroesdata.stormmod/base.stormdata/GameData/EmoticonPackData.xml`
- `mods/heroesdata.stormmod/base.stormdata/GameData/EmoticonData.xml`
- `mods/heroesdata.stormmod/enus.stormdata/LocalizedData/GameStrings.txt`
- `mods/heroes.stormmod/base.stormassets/Assets/Textures/storm_emoji_*.dds`

### Usage

`python extract_emoji.py path_to_mods [enus]`

Images will be in the "emoji" folder.

## MissingSkinFinder ![:orphoops:](https://i.imgur.com/hFl088z.png)

Who'se that variation?!

Parses catalog data to list rewards and search for missing/unobtainable rewards.

### Usage

`python catalog.py path_to_mods path_to_programdata_blizzardent [enus [us]]`

## HeroTrivia ![:pachgold:](https://i.imgur.com/ArA710D.png)

Now you can know how tiny hitboxes are too.

Parses catalog data to list miscellaneous info from heroes.

### Usage

`python hero_trivia.py path_to_mods [enus]`
