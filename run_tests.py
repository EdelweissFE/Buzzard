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

import argparse
import os

import numpy as np

from buzzard.optimizer import runOptimization
from buzzard.reader import readConfig, readConfigFromJson

createResults = False
tests = ["examples/LinearElastic/config.py"]

wd = os.getcwd()

if __name__ == "__main__":

    failedTests = 0

    for test in tests:

        if test.endswith(".py"):
            config = readConfig(test)
        elif test.endswith(".json"):
            config = readConfigFromJson(test)
        else:
            raise Exception("File type of config file must be .py or .json")

        head_tail = os.path.split(test)
        os.chdir(head_tail[0])

        args = argparse.Namespace
        args.parallel = 0
        args.createPlots = False

        result = runOptimization(config, args)

        if createResults:
            np.savetxt("results_ref.txt", result.x)

        reference = np.loadtxt("results_ref.txt")

        if np.linalg.norm((result.x - reference) / reference) > 1e-6:
            failedTests += 1

        os.chdir(wd)

    print("{:} test(s) failed!".format(failedTests))
    if failedTests == 0:
        exit(0)
    else:
        exit(1)
