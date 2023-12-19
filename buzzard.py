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

import buzzard.core.optimizer
import buzzard.utils.journal
from buzzard.core.optimizer import runOptimization
from buzzard.utils.journal import printHeader
from buzzard.utils.reader import readConfig, readConfigFromJson

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="buzzard",
        description="A tool for optimizing (material) parameters for finite element simulations",
    )

    parser.add_argument(
        "file",
        type=str,
        nargs=1,
    )
    parser.add_argument("--parallel", action="store_true", default=False)
    parser.add_argument("--createPlots", action="store_true", default=False)
    parser.add_argument("--quiet", action="store_true", default=False)

    args = parser.parse_args()

    buzzard.core.optimizer.executeSimulationsInParallel = args.parallel
    buzzard.core.optimizer.createPlots = args.createPlots
    buzzard.utils.journal.quiet = args.quiet

    printHeader()

    configFile = args.file[0]
    root, ext = os.path.splitext(configFile)
    if ext == ".py":
        config = readConfig(configFile)
    elif ext == ".json":
        config = readConfigFromJson(configFile)
    else:
        raise Exception("File type of config file must be .py or .json")

    result = runOptimization(config)
