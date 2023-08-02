import xml.etree.ElementTree as ET

def get_tree (file_name):
    #
    tree = ET.parse(file_name)
    return tree

def get_root (tree):
    root = tree.getroot()
    return root

def get_measurements(root, kword):
    losses = {}
    for measurements in root.findall(kword):
        for measurement in measurements:
            freq = measurement.find("Frequency").text
            gain = measurement.find("Gain").text
            gain = abs(float(gain))
            losses[freq] = gain
    return losses

if __name__ == "__main__":
    tree = get_tree("Cableloss Converter\Calibration Files\AA2213_15cm_Flex_Ant1.xml")
    root = get_root(tree)
    get_measurements(root, 'Measures')
