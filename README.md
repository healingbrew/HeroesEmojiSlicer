# HeroesEmojiSlicer
Slice and Dice ![:abacool:](https://i.imgur.com/cEUaVLY.png)

Download [here](https://github.com/naomichan/HeroesEmojiSlicer/archive/master.zip)

# Installation

- Python 2.7
- `pip install Pillow`
- ImageMagick (for conversion)

# Extract

Destination is `data`

- `mods/heroesdata.stormmod/base.stormdata/GameData/EmoticonPackData.xml`
- `mods/heroesdata.stormmod/base.stormdata/GameData/EmoticonData.xml`
- `mods/heroesdata.stormmod/enus.stormdata/LocalizedData/GameStrings.txt`

Destination is `data/sheets`

- `mods/heroes.stormmod/base.stormassets/Assets/Textures/storm_emoji_*.dds`

So the `data` directory should look like

```
data/EmoticonPackData.xml
data/EmoticonData.xml
data/GameStrings.txt
data/sheets/storm_emoji_abathur_sheet.dds
```

# Conversion

In `data/sheets` execute `mogrify -format png *.dds` (ImageMagick must be in the PATH)

# Usage

`python slice.py` (requires both Python and ImageMagick to be in the PATH)

Images will be in the "emoji" folder.
