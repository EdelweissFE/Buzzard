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
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Union

import numpy as np
from optimparallel import minimize_parallel
from scipy.optimize import Bounds, OptimizeResult, minimize

from .identification import Identification
from .journal import infoMessage, message, printLine, printSepline
from .plotters import plotOptimizationResults
from .simulation import Simulation


def runOptimization(config: dict, args: argparse.Namespace) -> OptimizeResult:
    """execute parameter identification"""
    method, options = getScipySettings(config)

    initialParameters, lowerBounds, upperBounds = collectIdentificationsFromConfig(config)

    collectSimulationsFromConfig(config)

    printSepline()
    infoMessage("call scipy minimize function ...")
    printSepline()

    # execute optimization
    tic = time.time()

    if args.parallel > 1:
        res = minimize_parallel(
            getResidualForMultipleSimulations,
            initialParameters,
            args=(args),
            bounds=Bounds(lowerBounds, upperBounds),
            options=options,
            callback=minimizerCallbackFunction,
        )
    else:
        res = minimize(
            getResidualForMultipleSimulations,
            initialParameters,
            args=(args),
            bounds=Bounds(lowerBounds, upperBounds),
            method=method,
            options=options,
            callback=minimizerCallbackFunction,
        )

    toc = time.time()

    printSepline()
    infoMessage("time in minimize function: " + str(round(toc - tic, 4)) + " seconds")

    printSepline()
    infoMessage("writing optimal parameters to optimalParameters.txt ... ")

    with open("optimalParameters.txt", "w+") as f:
        for x, ide in zip(res.x, Identification.active_identifications):
            f.write(str(x) + "\t#" + ide.name + "\n")
            message("   {:4.4e}".format(x) + " " + ide.name)

    if args.createPlots:
        printLine()
        message(" plot results ... ")
        plotOptimizationResults(initialParameters, res.x)

    printSepline()

    return res


def getScipySettings(config: dict) -> Union[str, dict]:

    method = None
    options = {"disp": True}

    if "scipysettings" in config:
        if "method" in config["scipysettings"]:
            method = config["scipysettings"]["method"]
        if "options" in config["scipysettings"]:
            options = config["scipysettings"]["options"]

    return method, options


def collectIdentificationsFromConfig(config: dict):

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

    message(" found " + str(len(Identification.active_identifications)) + " active parameter(s) to identify")

    return initialX, lb, ub


def collectSimulationsFromConfig(config):

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
    infoMessage("found " + str(len(Simulation.all_simulations)) + " active simulations(s)")


def getResidualForMultipleSimulations(params: np.ndarray, args) -> float:

    yErr = np.array([])

    if args.parallel in [1, 3]:
        nSim = len(Simulation.all_simulations)
        with ProcessPoolExecutor(max_workers=nSim) as executor:
            future_res = {executor.submit(sim.computeErrorVector, params): sim for sim in Simulation.all_simulations}

            for future in as_completed(future_res):
                yErr = np.append(yErr, future.result())

    else:
        for sim in Simulation.all_simulations:
            yErr = np.append(yErr, sim.computeErrorVector(params))

    residual = np.linalg.norm(yErr)

    return residual


def minimizerCallbackFunction(x: np.ndarray, *args):

    printLine()
    infoMessage("current parameters ...")
    for i, val in enumerate(x):
        message(" -->", Identification.active_identifications[i].name, "= {:e}".format(val))
    printLine()
