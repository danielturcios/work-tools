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
    # parses throught the root node of a tree using the following path: 'Root'-> kword('Measurements') ->'Measurement'
    # At each Measurement object, store the frequency and gain into dictionary 'losses'
    # then returns losses, a dictionary with freq as keys and the respective gain as values 
    losses = {}
    for measurements in root.findall(kword):
        for measurement in measurements:
            freq = measurement.find("Frequency").text
            gain = measurement.find("Gain").text
            gain = abs(float(gain))
            losses[freq] = gain
    return losses

def generate_measurement (ant):
    # Generate a dictionary based off the specific antenna cableloss file. 
    # Parameter ant is a string that completes the filename that will be converted from xml to a dict
    tree = get_tree("Cableloss Converter\Calibration Files\AA2213_15cm_Flex_Ant" + ant + ".xml")
    root = get_root(tree)
    ant_loss = get_measurements(root, 'Measures')
    return ant_loss

def generate_all_measurements ():
    # generates a dictionary with the antenna names as keys and a dictionary of the respective
    # freq/gains for each antenna. Also adds a default antenna cableloss key that contains a dictionary value
    # consisting of all shared frequencies and 1 gain by default
    all_measures = {}
    default = {}

    all_measures['Ant1'] = generate_measurement ('1')
    all_measures['Ant2'] = generate_measurement ('2')
    all_measures['Ant3'] = generate_measurement ('3')
    all_measures['Ant4'] = generate_measurement ('4')
    all_measures['Ant7'] = generate_measurement ('7')
    all_measures['Ant8'] = generate_measurement ('8')
    all_measures['Ant9'] = generate_measurement ('9')

    for freq in all_measures['Ant1']:
        default[freq] = 1

    all_measures['default'] = default
    return all_measures

if __name__ == "__main__":
    #Test Step
    ant_losses = generate_all_measurements()
