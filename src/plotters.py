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

import matplotlib.pyplot as plt

from .simulation import Simulation
from .journal import message


def plotOptimizationResults(initialParams, optParams):

    for sim in Simulation.all_simulations:

        initialX, initialY = sim.run(initialParams)
        optX, optY = sim.run(optParams)

        plt.figure()
        plt.plot(sim.data[:, 0], sim.data[:, 1], "x", label="given data", markersize=5)
        plt.plot(initialX, initialY, label="initial params")
        plt.plot(optX, optY, label="optimal params")
        plt.legend()
        plt.grid()
        plt.xlim(min(sim.data[:, 0]), max(sim.data[:, 0]))
        plt.savefig(sim.name + ".png")
        message(" --> " + sim.name + ".png")
