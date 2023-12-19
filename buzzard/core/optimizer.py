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

import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Tuple, Union

import numpy as np
from scipy.optimize import Bounds, OptimizeResult

from buzzard.core.identification import Identification
from buzzard.core.simulation import Simulation
from buzzard.interfaces.scipy import (
    availableOptimizationMethods,
    callSciPyGlobalOptimization,
    callSciPyMinimize,
)
from buzzard.utils.journal import (
    errorMessage,
    infoMessage,
    message,
    printLine,
    printSepline,
)
from buzzard.utils.plotters import plotOptimizationResults

executeSimulationsInParallel = False
createPlots = False


def runOptimization(config: dict) -> OptimizeResult:
    """
    Core function which executes parameter identification.

    Parameters
    ----------
    dict config
        Dictionary containing the information of the Buzzard input.

    Returns
    -------
    scipy.optimize.OptimizeResult
    """

    method, options = getOptimizationMethodAndOptions(config)

    initialParameters, lowerBounds, upperBounds = collectParametersToIdentify(config)

    collectSimulations(config)

    printSepline()
    infoMessage("call scipy minimize function ...")
    printSepline()

    # execute optimization
    tic = time.time()
    try:
        if method in availableOptimizationMethods.get("local"):
            res = callSciPyMinimize(
                getResidualForMultipleSimulations,
                initialParameters,
                Bounds(lowerBounds, upperBounds),
                method,
                options,
            )
        elif method in availableOptimizationMethods.get("global"):
            res = callSciPyGlobalOptimization(
                getResidualForMultipleSimulations,
                [(min_, max_) for min_, max_ in zip(lowerBounds, upperBounds)],
                method,
                options,
            )
        else:
            errorMessage(
                "Requested optimization method '{:}' not available!".format(method)
            )
            infoMessage("available methods are", availableOptimizationMethods)

            raise Exception(
                "Requested optimization method '{:}' not available!".format(method)
            )

    except KeyboardInterrupt:
        infoMessage("interrupted by user")
        exit(0)

    toc = time.time()

    printSepline()
    infoMessage("total time for optimization: " + str(round(toc - tic, 4)) + " seconds")

    printSepline()
    infoMessage("writing optimal parameters to optimalParameters.txt ... ")

    with open("optimalParameters.txt", "w+") as f:
        for x, ide in zip(res.x, Identification.active_identifications):
            f.write(str(x) + "\t#" + ide.name + "\n")
            message("   {:4.4e}".format(x) + " " + ide.name)

    if createPlots:
        printLine()
        message(" plot results ... ")
        plotOptimizationResults(initialParameters, res.x)

    printSepline()

    return res


def getOptimizationMethodAndOptions(config: dict) -> Union[str, dict]:
    """
    Extracts the optimization method and respective options from the input dictionary.

    Parameters
    ----------
    dict config
        Dictionary containing the information of the Buzzard input.

    Returns
    -------
    Union[str,dict]
    """

    method = config["scipysettings"].get("method", None)
    options = config["scipysettings"].get("options", {})

    return method, options


def collectParametersToIdentify(config: dict) -> Tuple[np.ndarray, list, list]:
    initialX = []
    lb = []
    ub = []

    printSepline()
    message(" collecting parameters to identify ...")
    printLine()

    if "identification" in config:
        for ideName, ideConfig in config["identification"].items():
            # skip inactive identifications
            ide = Identification(ideName, ideConfig)
            if ide.active:
                initialX.append(ide.start)
                lb.append(ide.min)
                ub.append(ide.max)

                message(" " + ide.name + " (active) ")
                message("   start=" + str(ide.start))
                message("     min=" + str(ide.min))
                message("     max=" + str(ide.max))

            else:
                message(" " + ide.name + " (inactive) ")
                message("   value=" + str(ide.start))

            printLine()
    else:
        raise Exception("no parameter(s) found to identify")

    message(
        "found ",
        str(len(Identification.active_identifications)),
        " active parameter(s) to identify",
    )

    return initialX, lb, ub


def collectSimulations(config):
    printSepline()
    infoMessage(" collecting simulations ...")
    printLine()

    if "simulations" in config:
        for name in config["simulations"]:
            # skip inactive simulations
            if "active" in config["simulations"][name].keys():
                if config["simulations"][name]["active"] is False:
                    message("  -->  " + name + " (inactive)")
                    continue

            message("  -->  " + name + " (active)")
            Simulation(name, config["simulations"][name])

    else:
        raise Exception("no simulations found")

    printLine()
    infoMessage(
        "found " + str(len(Simulation.all_simulations)) + " active simulations(s)"
    )


def getResidualForMultipleSimulations(params: np.ndarray) -> float:
    yErr = np.array([])

    # workaround for differential evolution

    if executeSimulationsInParallel is True:
        nSim = len(Simulation.all_simulations)
        with ProcessPoolExecutor(max_workers=nSim) as executor:
            future_res = {
                executor.submit(sim.computeWeightedResidual, params): sim
                for sim in Simulation.all_simulations
            }

            for future in as_completed(future_res):
                yErr = np.append(yErr, future.result())

    else:
        for sim in Simulation.all_simulations:
            yErr = np.append(yErr, sim.computeWeightedResidual(params))

    return np.sum(yErr)
