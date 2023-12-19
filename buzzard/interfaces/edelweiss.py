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
from typing import Union

import numpy as np

# load necessary EdelweissFE functionality
# if you do not have EdelweissFE installed, you can get it from
# github.com/edelweissfe/edelweissfe
from fe.drivers.inputfiledrivensimulation import finiteElementSimulation  # noqa: E402
from fe.utils.inputfileparser import parseInputFile  # noqa: E402

from buzzard.core.identification import Identification
from buzzard.core.simulation import Simulation


def getInputDictWithCurrentParameters(currParams: np.ndarray, sim: Simulation) -> dict:
    """
    Creates an input dictionary with the current parameters.

    Parameters
    ----------
    numpy.ndarray currParams
        An array with the current parameters.
    buzzard.simulation.Simulation sim
        The respective simulation object.

    Returns
    -------
    dict
        Input dictionary for EdelweissFE.
    """

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


def evaluateEdelweissSimulation(currParams: np.ndarray, sim: Simulation) -> Union[np.ndarray, np.ndarray]:
    """
    Evaluates a single EdelweissFE simulation with certain parameters.

    Parameters
    ----------

    numpy.ndarray currParams
        An array with the current parameters.
    buzzard.simulation.Simulation sim
        The respective simulation object.

    Returns
    -------
    numpy.ndarray
        x-data for the simulation.
    numpy.ndarray
        y-data for the simulation.
    """

    # replace parameters for the simulation
    inp = getInputDictWithCurrentParameters(currParams, sim)

    # execute simulation
    femodel, fieldOutputController = finiteElementSimulation(inp, verbose=False)

    try:
        if sim.fieldoutputX == sim.fieldoutputY:
            # get time history as x value if only one fieldoutput is given
            x = np.array(fieldOutputController.fieldOutputs[sim.fieldoutputX].timeHistory).ravel()
            y = np.array(fieldOutputController.fieldOutputs[sim.fieldoutputY].result).ravel()
        else:
            x = np.array(fieldOutputController.fieldOutputs[sim.fieldoutputX].result).ravel()
            y = np.array(fieldOutputController.fieldOutputs[sim.fieldoutputY].result).ravel()
    except Exception as e:
        print("simulation failed !!!: Exception: ", e)
        x = None
        y = None

    return x, y
