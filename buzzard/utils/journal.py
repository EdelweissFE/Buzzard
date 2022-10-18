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

maxCharCentered = 70
maxCharJustified = 68

quiet = False


def printHeader():
    """Prints the program header."""
    printSepline()
    printCenteredLine("This is")
    printCenteredLine("")
    printCenteredLine(" ____                             _ ")
    printCenteredLine("| __ ) _   _ __________ _ _ __ __| |")
    printCenteredLine("|  _ \\| | | |_  /_  / _` | '__/ _` |")
    printCenteredLine("| |_) | |_| |/ / / / (_| | | | (_| |")
    printCenteredLine("|____/ \\__,_/___/___\\__,_|_|  \\__,_|")
    printCenteredLine("")
    printCenteredLine("a part of")
    printCenteredLine("")
    printCenteredLine("-- EdelweissFE --")
    printCenteredLine("github.com/EdelweissFE")
    printCenteredLine("")
    printSepline()


def infoMessage(*args):
    """Prints an info message."""
    message(*("INFO:", *args))


def errorMessage(*args):
    """Prints an error message."""
    message(*("ERROR:", *args))


def message(*args):
    """Prints a message to the terminal with fixed format."""
    if quiet is False:
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
    """Prints a separation line."""
    printCenteredLine(maxCharCentered * "=")


def printLine():
    """Prints a simple line."""
    printCenteredLine(maxCharCentered * "-")


def printCenteredLine(string: str):
    """Prints a string which is centered."""
    if quiet is False:
        print("|{:^{}s}|".format(string, maxCharCentered))


def printJustifiedLine(string: str):
    """Prints a string which is justified."""
    if quiet is False:
        print("| {:<{}s} |".format(string, maxCharJustified))
