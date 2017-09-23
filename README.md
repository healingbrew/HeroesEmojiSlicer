# HeroesEmojiSlicer
Slice and Dice ![:abacool:](//i.imgur.com/cEUaVLY.png)

# Installation

- Python 2.7
- `pip install Pillow`

# Extract

Destination is `data`

- `mods/heroesdata.stormmod/base.stormdata/GameData/EmoticonPackData.xml`
- `mods/heroesdata.stormmod/base.stormdata/GameData/EmoticonData.xml`
- `mods/heroesdata.stormmod/enus.stormdata/LocalizedData/GameStrings.txt`

Destination is `data/sheets`

- `mods/heroes.stormmod/base.stormassets/Assets/Textures/storm_emoji_*.dds`

# Conversion

In `data/sheets`

`mogrify -format png *.dds`

# Usage

`python27 slice.py`

Images will be in the "emoji" folder.
