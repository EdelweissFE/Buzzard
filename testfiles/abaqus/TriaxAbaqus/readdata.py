import sys

import numpy as np
from odbAccess import openOdb

"""
Paul Hofer
2021-04-30
"""

odb = openOdb(path=sys.argv[1])
exportFileName = sys.argv[2]

stepid = "loading"

# define output x
xkeys = {
    "foutid": "U",  # displacements U
    "foutidx": 1,  # in y direction
    "nsetid": "nodeontopsurf".upper(),  # name of set for summing up results
    "nset": "",  # node set object
    "arrayidx": 0,
}  # first column in output file

ykeys = {
    "foutid": "RF",
    "foutidx": 1,
    "nsetid": "topsurf".upper(),
    "nset": "",
    "arrayidx": 1,
}

keys = {"x": xkeys, "y": ykeys}

for key in keys:
    # for Assembly-Set:
    keys[key]["nset"] = odb.rootAssembly.nodeSets[keys[key]["nsetid"]]
    # for Part-Set:
    # nSet = odb.rootAssembly.instances[partname].nodeSets[nSetname]

# read output from .odb
output = np.array([])
output.shape = (0, 2)
vals = np.array([[0.0, 0.0]])
for frame in odb.steps[stepid].frames:
    vals[0][0] = 0.0
    vals[0][1] = 0.0
    for key in keys:
        fieldOutput = frame.fieldOutputs[keys[key]["foutid"]].getSubset(region=keys[key]["nset"])
        for node in fieldOutput.values:
            vals[0][keys[key]["arrayidx"]] += node.data[keys[key]["foutidx"]]
    output = np.concatenate((output, vals))

# write output to file
np.savetxt(exportFileName, output)
