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

import numpy as np
import sys
import os
import subprocess
import random as rd

from .identification import Identification
from .journal import message

# abaqusExecuteable = 'singularity exec /home/ad/constitutiveModelling/abaqus-2019-centos-7.simg abaqus'


def evaluateAbaqusSimulation(currParams, sim):

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

    with open(randomFileName + ".inp", "w+") as n:
        n.write(data)

    # execute simulation

    abaqusExecuteable = sim.executeable
    cpus = sim.cpus

    simCommand = " ".join(
        [abaqusExecuteable, "-j", randomFileName, "interactive", "cpus=" + str(cpus)]
    )

    success = runCommandAndCatchError(simCommand)

    if success:
        runCommandAndCatchError(
            " ".join(
                [
                    abaqusExecuteable,
                    "python",
                    sim.postProcessingScript,
                    randomFileName + ".odb",
                    randomFileName + ".out",
                ]
            )
        )
        simdata = np.loadtxt(randomFileName + ".out")
        x = simdata[:, 0]
        y = simdata[:, 1]
    else:
        x = None
        y = None

    # remove all generated files
    os.system("rm -r {name}*".format(name=randomFileName))

    return x, y


def runCommandAndCatchError(command):

    com = [c.replace("'", "") for c in command.split(" ")]
    pipe = subprocess.Popen(
        com, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False
    )

    text = ""
    for i in pipe.communicate():
        text += i.decode("utf-8")

    if "error" in text.lower():
        message(str(com))
        message(text)
        return False

    else:
        return True
