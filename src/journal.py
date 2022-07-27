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

from textwrap import wrap

from rich import print

maxCharCentered = 70
maxCharJustified = 68


def printHeader():
    printSepline()
    printCenteredLine("BUZZARD")
    printCenteredLine("")
    printCenteredLine("-- MaterialModelingToolbox --")
    printCenteredLine("github.com/MAteRialMOdelingToolbox")
    printCenteredLine("")
    printSepline()


def infoMessage(*args):
    message(*("INFO:", *args))


def errorMessage(*args):
    message(*("ERROR:", *args))


def message(*args):
    if args:
        string = str(args[0])
        for arg in args[1:]:
            string += " " + str(arg)
        if len(string) < maxCharJustified:
            printJustifiedLine(string)
        else:
            stringList = wrap(string, maxCharJustified - 3)
            printJustifiedLine(stringList[0])
            for string in stringList[1:]:
                printJustifiedLine("..." + string)
    else:
        printJustifiedLine(" ")


def printSepline():
    printCenteredLine(maxCharCentered * "=")


def printLine():
    printCenteredLine(maxCharCentered * "-")


def printCenteredLine(string):
    print("|{:^{}s}|".format(string, maxCharCentered))


def printJustifiedLine(string):
    print("| {:<{}s} |".format(string, maxCharJustified))
