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
import similaritymeasures
from scipy import interpolate

from buzzard.utils.journal import errorMessage, infoMessage


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
        self.flipXY = config.get("flipXY", False)
        self.weight = config.get("weight", 1.0)

        if type(config["data"]) is list:
            self.data = [np.loadtxt(d) for d in config["data"]]
        else:
            self.data = np.loadtxt(config["data"])

        if self.flipXY:
            self.data[:, [1, 0]] = self.data[:, [0, 1]]

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

        x = None
        y = None

        if self.type == "edelweiss":
            from buzzard.interfaces.edelweiss import evaluateEdelweissSimulation

            x, y = evaluateEdelweissSimulation(currParams, self)

        elif self.type == "abaqus":
            from buzzard.interfaces.abaqus import evaluateAbaqusSimulation

            x, y = evaluateAbaqusSimulation(currParams, self)

        else:
            errorMessage(
                "Unknown simulation type;",
                "possible types are:",
                "'edelweiss' and",
                "'abaqus',",
            )
            exit()

        if self.flipXY:
            return y, x

        return x, y

    def computeResidualForSingleDataSet(self, simX: np.ndarray, simY: np.ndarray, data: np.ndarray) -> float:
        if self.errorType == "relative":
            yErr = np.array([])
            try:
                xySim = self.interpolateSimulationResults(simX, simY)

                for i in range(len(data[:, 1])):
                    if data[i, 1] == 0:
                        continue

                    yErr = np.append(
                        yErr,
                        (data[i, 1] - xySim(data[i, 0])) / data[i, 1],
                    )
                return self.weight * np.linalg.norm(yErr)

            # catch error if simulation failed
            except ValueError:
                return 1e12

        # compute relative error vector
        elif self.errorType == "absolute":
            yErr = np.array([])
            xySim = self.interpolateSimulationResults(simX, simY)

            for i in range(len(data[:, 1])):
                yErr = np.append(yErr, data[i, 1] - xySim(data[i, 0]))

            return self.weight * np.linalg.norm(yErr)

        elif self.errorType == "area-between":
            # find index to start and end
            start = 0
            end = 0
            for xItem in simX:
                if xItem < max(data[:, 0]):
                    end += 1
                    if xItem < min(data[:, 0]):
                        start += 1
                else:
                    break

            simData = np.vstack([simX[start:end], simY[start:end]]).T

            return self.weight * similaritymeasures.area_between_two_curves(data, simData)

        elif self.errorType == "frechet-distance":
            # find index to start and end
            start = 0
            end = 0
            for xItem in simX:
                if xItem < max(self.data[:, 0]):
                    end += 1
                    if xItem < min(self.data[:, 0]):
                        start += 1
                else:
                    break

            sim = np.vstack(
                [
                    simX[start:end],
                    simY[start:end],
                ]
            ).T
            exp = np.vstack(
                [
                    self.data[:, 0],
                    self.data[:, 1],
                ]
            ).T

            return self.weight * similaritymeasures.frechet_dist(exp, sim)

        elif self.errorType == "partial-curve-mapping":
            # find index to start and end
            start = 0
            end = 0

            for xItem in simX:
                if xItem < max(data[:, 0]):
                    end += 1
                    if xItem < min(data[:, 0]):
                        start += 1
                else:
                    break

            sim = np.vstack([simX[start:end], simY[start:end]]).T
            exp = np.vstack([data[:, 0], data[:, 1]]).T

            return self.weight * similaritymeasures.pcm(exp, sim)

        else:
            errorMessage(
                "Unknown type for error calculation;",
                "possible types are:",
                "'relative',",
                "'absolute',",
                "'area-between',",
                "'frechet-distance', and",
                "'partial-curve-mapping'",
            )
            exit()

    def computeWeightedResidual(self, currParams: np.ndarray) -> np.ndarray:
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
            return 1e12

        residuals = []

        for i in range(len(x[0, :])):
            residuals.append(self.computeResidualForSingleDataSet(x[:, i], y[:, i], self.data[i]))

        return np.linalg.norm(np.array(residuals))

    def interpolateSimulationResults(self, x: np.ndarray, y: np.ndarray) -> interpolate.interp1d:
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

        return interpolate.interp1d(np.array(xlist, dtype=object), np.array(ylist, dtype=object))
