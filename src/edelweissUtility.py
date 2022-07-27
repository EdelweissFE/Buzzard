import numpy as np
import sys
import os
import random as rd

edelweissPath = os.environ.get("EDELWEISS_PATH")
if edelweissPath is None:
    raise Exception("You need to specify the environment variable EDELWEISS_PATH")
sys.path.append(edelweissPath)
import fe
from fe.fecore import finiteElementSimulation
from fe.utils.inputfileparser import parseInputFile
from fe.utils.misc import mergeNumpyDataLines

from .identification import Identification


def readEdelweissInputfile(filename):

    inp = parseInputFile(filename)

    # flatten data lines for material data
    for n in range(len(inp["*material"])):
        inp["*material"][n]["data"] = mergeNumpyDataLines(inp["*material"][n]["data"])

    return inp


def setCurrentParams(currParams, sim):

    randomFileName = "_temp_" + str(rd.randint(0, 1e16))

    # create input for current parameters
    paramIDX = 0

    data = str(sim.inp)
    for ide in Identification.all_identifications:
        if ide.active:
            data = data.replace(ide.name, str(currParams[paramIDX]))
            paramIDX += 1
        else:
            data = data.replace(ide.name, str(ide.start))

    with open(randomFileName + ".inp", "w+") as f:
        f.write(data)

    return readEdelweissInputfile(randomFileName + ".inp")


def evaluateEdelweissSimulation(currParams, sim):

    # replace parameters for the simulation
    inp = setCurrentParams(currParams, sim)

    # execute simulation
    success, U, P, fieldOutputController = finiteElementSimulation(inp, verbose=False)

    if success:

        if sim.fieldoutputX == sim.fieldoutputY:
            # get time history as x value if only one fieldoutput is given
            x = np.array(
                fieldOutputController.fieldOutputs[sim.fieldoutputX].timeHistory
            )
            y = np.array(fieldOutputController.fieldOutputs[sim.fieldoutputY].result)
        else:
            x = np.array(fieldOutputController.fieldOutputs[sim.fieldoutputX].result)
            y = np.array(fieldOutputController.fieldOutputs[sim.fieldoutputY].result)
    else:
        print("simulation failed !!!")
        x = None
        y = None

    return x, y
