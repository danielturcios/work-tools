import xml.etree.ElementTree as ET

def get_tree (file_name):
    # returns an ElementTree from the given filename
    tree = ET.parse(file_name)
    return tree

def get_root (tree):
    # returns the root of the given ELementTree object
    root = tree.getroot()
    return root

def get_measurements(root, kword):
    # parses throught the root node to using the following path 'Root'->'Measurements'->'Measurement'
    # At each Measurement object, store the frequency and gain into dictionary 'losses'
    # then returns losses
    losses = {}
    for measurements in root.findall(kword):
        for measurement in measurements:
            freq = measurement.find("Frequency").text
            gain = measurement.find("Gain").text
            gain = abs(float(gain))
            losses[freq] = gain
    return losses

def generate_measurement (ant):
    tree = get_tree("Cableloss Converter\Calibration Files\AA2213_15cm_Flex_Ant" + ant + ".xml")
    root = get_root(tree)
    ant_loss = get_measurements(root, 'Measures')
    return ant_loss



if __name__ == "__main__":
    #Test Step
    ant1_loss = generate_measurement ('1')
    for i in ant1_loss:
        print (i, ant1_loss[i])
