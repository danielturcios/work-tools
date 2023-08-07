import xml.etree.ElementTree as ET

header = "Frequency (MHz), Ant 1, Ant 2, Ant 3, Ant 4, Ant 1A, Ant 2A, Ant 3A, Ant 4A\n"
file_to_create = "AA2213_config1B.sploss"
config = "1B"

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

def create_file (file_name, header):
    # creates a new file or overwrite existing file with file_name and adds the header line (specified by global_parameter header)
    f = open(file_name, 'w+')
    f.write(header)
    return f

def create_loss_table (file, ant_config, ant_losses):
    line = ""
    for freq in ant_losses["default"]:
        line = str(freq) + ','
        for ant in ant_config:
            line += str(ant_losses[ant][freq]) + ','
        line = line[:-1] + '\n'
        file.write(line)
        line = ""

def create_sploss_table (file, config, ant_losses) :
    ant_config = []
    if config.upper() == "1A":
        ant_config = ["Ant7", "Ant8", "Ant9", "Ant4", "Ant1", "Ant2", "Ant3", "default"]
    elif config.upper() == "1B":
        ant_config = ["Ant2", "Ant3", "Ant4", "default", "Ant1", "default", "default", "default"]
    else:
        ant_config = ["default"] * 8
    create_loss_table(file, ant_config, ant_losses)

if __name__ == "__main__":
    #Test Step
    ant_losses = generate_all_measurements()
    file = create_file(file_to_create, header)
    create_sploss_table(file, config, ant_losses)
    file.close()