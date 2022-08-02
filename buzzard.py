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

from src.journal import printHeader
from src.optimizer import runOptimization
from src.reader import readConfig, readConfigFromJson

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
    parser.add_argument(
        "--parallel",
        type=int,
        default=0,
        choices=[0, 1, 2, 3],
        help="0: no parallelization (default);i"
        + "1: parallel execution of simulations;"
        + "2:run parallel minimize (L-BGFS method only);"
        "3: combines option 1 and 2 (L-BGFS method only)",
    )
    parser.add_argument("--createPlots", action="store_true", default=False)

    args = parser.parse_args()
    printHeader()

    configFile = args.file[0]
    root, ext = os.path.splitext(configFile)
    if ext == ".py":
        config = readConfig(configFile)
    elif ext == ".json":
        config = readConfigFromJson(configFile)
    else:
        raise Exception("File type of config file must be .py or .json")

    # set environment variables
    if "env_variables" in config.keys():
        for var, value in config["env_variables"].items():
            os.environ[var] = value

    success = runOptimization(config, args)
