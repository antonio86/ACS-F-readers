__author__ = 'antonioridi'

import os
import numpy as np

# reader to be placed at the same level of the ACS-F database.
# in this case, the folder is called 'ACS-F2'
directory = os.getcwd() + '/ACS-F2'
list_dir = [x[0] for x in os.walk(directory)]
list_dir = list_dir[1:]

list_xml = []
for dirnames in list_dir:
    list_filenames = [x[2] for x in os.walk(dirnames)][0]
    for filenames in list_filenames:
        if filenames.endswith(".mat"):
            cnt = 0
            tmp_mat = []
            for line in open(dirnames + '/' + filenames):
                li=line.strip()
                if not li.startswith("#"):
                    line_float = np.array(list(map(float, li.split(' '))))
                    tmp_mat.append(line_float)
                    cnt += 1
            list_xml.append(np.array(tmp_mat))

