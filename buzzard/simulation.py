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

from typing import Union

import numpy as np
from scipy.interpolate import interp1d
from similaritymeasures import area_between_two_curves, frechet_dist, pcm

from .journal import errorMessage, infoMessage


class Simulation:
    """
    The identification object stores information for one simulation for the optimization process.

    Parameters
    ----------
    str name
        Name of the simulation.
    dict config
        Dictionary which contains information about the simulation.
    """

    all_simulations = []
    """A list containing all simulations."""

    def __init__(self, name, config):

        self.name = name
        self.type = config["type"]

        if type(config["data"]) == list:
            self.data = np.concatenate(tuple([np.loadtxt(d) for d in config["data"]]), axis=0)
        else:
            self.data = np.loadtxt(config["data"])

        if "errorType" not in config.keys():
            self.errorType = "relative"
        else:
            self.errorType = config["errorType"]

        if self.type == "edelweiss":
            self.inp = open(config["input"]).read()
            self.fieldoutputX = config["simX"]
            self.fieldoutputY = config["simY"]
        elif self.type == "abaqus":
            self.inp = open(config["input"]).read()
            self.postProcessingScript = config["postProcessingScript"]
            self.executeable = config["executeable"]
            self.cpus = config["cpus"]
        Simulation.all_simulations.append(self)

    def run(self, currParams: np.ndarray) -> Union[np.ndarray, np.ndarray]:
        """
        Executes the simulation

        Parameters
        ----------
        numpy.ndarray currParams
            An array with the current parameters.

        Returns
        -------
        Union[numpy.ndarray,numpy.ndarray]
            Result of the simulation (x-data, y-data).
        """

        if self.type == "edelweiss":
            from .edelweissUtility import evaluateEdelweissSimulation

            x, y = evaluateEdelweissSimulation(currParams, self)

        elif self.type == "abaqus":
            from .abaqusUtility import evaluateAbaqusSimulation

            x, y = evaluateAbaqusSimulation(currParams, self)

        else:
            errorMessage(
                "Unknown simulation type;",
                "possible types are:",
                "'edelweiss' and",
                "'abaqus',",
            )
            exit()

        return x, y

    def computeErrorVector(self, currParams: np.ndarray) -> np.ndarray:
        """
        Computes the error vector for the simulation wrt the given data.

        Parameters
        ----------
        numpy.ndarray currParams
            An array with the current parameters.

        Returns
        -------
        numpy.ndarray
            Array containing the errors between given data and simulation.
        """
        x, y = self.run(currParams)

        if type(x) is not np.ndarray:
            infoMessage(
                "Simulation {sim} failed with the following parameters:{params}".format(
                    sim=self.name, params=currParams
                )
            )
            return np.array([1e12])
        yErr = np.array([])

        # compute relative error vector
        if self.errorType == "relative":

            xySim = self.interpolateSimulationResults(x, y)
            for i in range(len(self.data[:, 1])):
                if self.data[i, 1] == 0:
                    continue
                try:
                    yErr = np.append(
                        yErr,
                        (self.data[i, 1] - xySim(self.data[i, 0])) / self.data[i, 1],
                    )
                except Exception as e:
                    infoMessage(e)

        # compute relative error vector
        elif self.errorType == "absolute":

            xySim = self.interpolateSimulationResults(x, y)
            for i in range(len(self.data[:, 1])):
                try:
                    yErr = np.append(yErr, self.data[i, 1] - xySim(self.data[i, 0]))
                except Exception as e:
                    print(e)

        elif self.errorType == "area-between":

            # find index to start and end
            start = 0
            end = 0
            for xItem in x:

                if xItem < max(self.data[:, 0]):
                    end += 1
                    if xItem < min(self.data[:, 0]):
                        start += 1
                else:
                    break

            simData = np.vstack([x[start:end], y[start:end]]).T
            yErr = np.append(yErr, area_between_two_curves(self.data, simData))

        elif self.errorType == "frechet-distance":

            # find index to start and end
            start = 0
            end = 0
            for xItem in x:

                if xItem < max(self.data[:, 0]):
                    end += 1
                    if xItem < min(self.data[:, 0]):
                        start += 1
                else:
                    break

            sim = np.vstack(
                [
                    x[start:end] / max(abs(self.data[:, 0])),
                    y[start:end] / max(abs(self.data[:, 1])),
                ]
            ).T
            exp = np.vstack(
                [
                    self.data[:, 0] / max(abs(self.data[:, 0])),
                    self.data[:, 1] / max(abs(self.data[:, 1])),
                ]
            ).T

            val = frechet_dist(exp, sim)

            yErr = np.append(yErr, val)

        elif self.errorType == "partial-curve-mapping":

            # find index to start and end
            start = 0
            end = 0
            for xItem in x:

                if xItem < max(self.data[:, 0]):
                    end += 1
                    if xItem < min(self.data[:, 0]):
                        start += 1
                else:
                    break

            sim = np.vstack([x[start:end], y[start:end]]).T
            exp = np.vstack([self.data[:, 0], self.data[:, 1]]).T

            val = pcm(exp, sim)

            yErr = np.append(yErr, val)

        else:
            errorMessage(
                "Unknown type for error calculation;",
                "possible types are:",
                "'relative',",
                "'absolute',",
                "'area-between',",
                "'frechet_dist', and",
                "'partial-curve-mapping'",
            )
            exit()

        return yErr

    def interpolateSimulationResults(self, x: np.ndarray, y: np.ndarray) -> interp1d:
        """
        Interpolates simulation results taking into account decreasing x-data.

        Parameters
        ----------
        numpy.ndarray x
            x-data for interpolation
        numpy.ndarray y
            y-data for interpolation

        Returns
        -------
        scipy.interpolate.interp1d
            interpolation of x and y
        """

        xlist = [x[0]]
        ylist = [y[0]]

        if x[0] > x[-1]:
            for i, val in enumerate(x[1:]):
                if x[i + 1] < x[i]:
                    xlist.append(float(val))
                    ylist.append(float(y[i + 1]))

        else:
            for i, val in enumerate(x[1:]):
                if x[i + 1] > x[i]:
                    xlist.append(float(val))
                    ylist.append(float(y[i + 1]))

        return interp1d(xlist, ylist)
