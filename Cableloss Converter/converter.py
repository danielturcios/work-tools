import xml.etree.ElementTree as ET

def parseTree (fileName):
    tree = ET.parse(fileName)
    root = tree.getroot()
    return root

if __name__ == "__main__":
    root = parseTree("Cableloss Converter\Calibration Files\AA2213_15cm_Flex_Ant1.xml")
    print (root)
