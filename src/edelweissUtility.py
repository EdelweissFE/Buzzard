# -*- coding: utf-8 -*-
#  ---------------------------------------------------------------------
#
#  ____                             _
# | __ ) _   _ __________ _ _ __ __| |
# |  _ \| | | |_  /_  / _` | '__/ _` |
# | |_) | |_| |/ / / / (_| | | | (_| |
# |____/ \__,_/___/___\__,_|_|  \__,_|
#
#
#  Unit of Strength of Materials and Structural Analysis
#  University of Innsbruck,
#  2021 - today
#
#  Alexander Dummer alexander.dummer@uibk.ac.at
#
#  This file is part of Buzzard.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  The full text of the license can be found in the file LICENSE.md at
#  the top level directory of Buzzard.
#  ---------------------------------------------------------------------

import os
import random as rd
import sys

import numpy as np

from .identification import Identification

edelweissPath = os.environ.get("EDELWEISS_PATH")
if edelweissPath is None:
    raise Exception("You need to specify the environment variable EDELWEISS_PATH")
sys.path.append(edelweissPath)
from fe.fecore import finiteElementSimulation  # noqa: E402
from fe.utils.inputfileparser import parseInputFile  # noqa: E402


def setCurrentParams(currParams, sim):

    randomFileName = "_temp_" + str(rd.randint(0, 1e16)) + ".inp"

    paramIDX = 0

    data = str(sim.inp)
    for ide in Identification.all_identifications:
        if ide.active:
            data = data.replace(ide.name, str(currParams[paramIDX]))
            paramIDX += 1
        else:
            data = data.replace(ide.name, str(ide.start))

    with open(randomFileName, "w+") as f:
        f.write(data)

    currentInputDict = parseInputFile(randomFileName)

    os.system("rm {:}".format(randomFileName))

    return currentInputDict


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
