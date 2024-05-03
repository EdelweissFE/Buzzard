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
import seaborn as sns

from buzzard.core.simulation import Simulation
from buzzard.utils.journal import message

sns.set_theme(context="paper", style="ticks", font="Arial")


def plotOptimizationResults(initialParams, optParams):
    for sim in Simulation.all_simulations:
        initialX, initialY = sim.run(initialParams)
        optX, optY = sim.run(optParams)

        n = len(initialX[0, :])
        fig, axs = plt.subplots(1, n, figsize=(n * 5, 5))

        for i in range(n):
            ax = axs[i]
            ax.plot(sim.data[i][:, 0], sim.data[i][:, 1], "x", label="given data")
            ax.plot(initialX[:, i], initialY[:, i], label="initial params")
            ax.plot(optX[:, i], optY[:, i], label="optimal params")
            ax.set_title("Simulation: " + sim.name)
            ax.legend()
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.legend()
            ax.grid()

        plt.tight_layout()
        plt.savefig(sim.name + ".pdf")
        message(" --> " + sim.name + ".pdf")
