import xml.etree.ElementTree as ET

def Catalog(path):
    return ET.parse(path).getroot()

def IsHidden(dataset):
    for flag in dataset.findall("Flags"):
        if flag.get("index") == "Hidden" and flag.get("value") == "1": return True
    return False
