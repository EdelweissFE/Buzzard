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
import sys
import json
from .journal import message


def readConfigFromJson(jsonfile):
    message("reading config from {:}... ".format(jsonfile))

    with open(jsonfile, "r") as j:
        data = json.load(j)

    return data


def readConfig(configFile):
    message("reading config from {:}... ".format(configFile))

    (head, tail) = os.path.split(configFile)
    sys.path.append(head)
    (root, ext) = os.path.splitext(tail)
    config = __import__(root).config

    return config
