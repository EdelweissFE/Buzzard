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


class Identification:
    """
    The identification object stores information for one parameter which is defined to be optimized.

    Parameters
    ----------
    str name
        Name of the parameter. Has to be equal to the placeholder in the simulation input files.
    dict values
        Dictionary to define values for the parameter. Required keys are 'start', 'min', 'max' and 'active'.
    """

    all_identifications = []
    """A list containing all identification objects."""
    active_identifications = []
    """A list containing all active identification objects."""

    def __init__(self, name: str, values: dict):
        self.checkInput(name, values)

        self.active = False
        self.name = name
        self.start = values["start"]

        if values["active"]:
            self.min = values["min"]
            self.max = values["max"]
            self.active = True
            Identification.active_identifications.append(self)

        Identification.all_identifications.append(self)

    def checkInput(self, name: str, values: dict):
        """Input check for Identification object initialization"""
        if not type(name) is str:
            raise Exception("name of the identification object must be a string")

        requiredKeys = ("start", "min", "max", "active")
        if not all(key in values for key in requiredKeys):
            raise Exception("one or more required keys are not provided for {:}".format(name))
