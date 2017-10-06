@ECHO OFF

mogrify -format png data/sheets/*.dds
python slice.py
