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
import time

import numpy as np
from rich import print

import buzzard.utils.journal
from buzzard.core.identification import Identification
from buzzard.core.optimizer import runOptimization
from buzzard.core.simulation import Simulation
from buzzard.utils.reader import readConfig, readConfigFromJson

createResults = False
buzzard.utils.journal.quiet = True


baseDir = "testfiles/edelweiss"

tests = sorted(next(os.walk(baseDir))[1])

wd = os.getcwd()

if __name__ == "__main__":

    os.environ["OMP_NUM_THREADS"] = "1"

    failedTests = 0

    for test in tests:
        # clear identifications and simulations
        Identification.all_identifications = []
        Identification.active_identifications = []
        Simulation.all_simulations = []
        try:
            config = readConfig(os.path.join(baseDir, test, "config.py"))

        except FileNotFoundError:
            try:
                config = readConfigFromJson(os.path.join(baseDir, test, "config.json"))
            except Exception as e:
                print("Test {:50} [red]FAILED[/] [{:<}]".format(test, e))
                continue

        testDir = os.path.join(baseDir, test)
        os.chdir(testDir)

        tic = time.time()
        result = runOptimization(config)
        toc = time.time()

        if createResults:
            np.savetxt("results_ref.txt", result.x)

        reference = np.loadtxt("results_ref.txt")

        if np.linalg.norm((result.x - reference) / reference) > 1e-6:
            failedTests += 1
            print("Test {:50} [red]FAILED[/] [{:2.1f}]".format(test, toc - tic))
        else:
            print("Test {:50} [green]PASSED[/] [{:2.1f}]".format(test, toc - tic))

        os.chdir(wd)

    print("\nSummary: {:} tests failed!".format(failedTests))

    if failedTests != 0:
        exit(1)
