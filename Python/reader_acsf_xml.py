__author__ = 'antonioridi'

import xml.etree.ElementTree as ET
import os
import numpy as np

# reader to be placed at the same level of the ACS-F database.
# in this case, the folder is called 'ACS-F2'
directory = os.getcwd() + '/ACS-F2'
list_dir = [x[0] for x in os.walk(directory)]
list_dir = list_dir[1:]

list_xml = []
list_name = []
for dirnames in list_dir:
    list_filenames = [x[2] for x in os.walk(dirnames)][0]
    for filenames in list_filenames:
        if filenames.endswith(".xml"):
            list_file = []
            list_name.append(filenames)
            tree = ET.parse(dirnames + '/' + filenames)
            root = tree.getroot()
            for child in root:
                if child.tag == 'signalCurve':
                    for child_2 in child:
                        tmp_xml = np.zeros(6)
                        tmp_xml[0] = float(child_2.get('freq'))
                        tmp_xml[1] = float(child_2.get('phAngle'))
                        tmp_xml[2] = float(child_2.get('power'))
                        tmp_xml[3] = float(child_2.get('reacPower'))
                        tmp_xml[4] = float(child_2.get('rmsCur'))
                        tmp_xml[5] = float(child_2.get('rmsVolt'))
                        list_file.append(tmp_xml)
            list_file = np.array(list_file)
            list_xml.append(list_file)

# now in list_xml there is a list of np.arrays