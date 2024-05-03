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

from typing import Callable, Sequence

import numpy as np
from optimparallel import minimize_parallel
from scipy import optimize

from buzzard.core.identification import Identification
from buzzard.utils.journal import infoMessage, message, printLine

availableOptimizationMethods = {
    "global": ["brute", "differential_evolution", "shgo", "dual_annealing"],
    "local": [
        "Nelder-Mead",
        "Powell",
        "L-BFGS-B",
        "L-BFGS-B-parallel",
        "TNC",
        "SLSQP",
        "trust-constr",
    ],
}


def callSciPyMinimize(
    f: Callable,
    initialParameters: np.ndarray,
    bounds: optimize.Bounds,
    method: str,
    options: dict,
):
    if method == "L-BFGS-B-parallel":
        return minimize_parallel(
            f,
            initialParameters,
            bounds=bounds,
            options=options,
            callback=minimizerCallbackFunction,
        )
    elif method == "TNC":
        return optimize.minimize(
            f,
            initialParameters,
            bounds=bounds,
            method=method,
            options=options,
            callback=minimizerCallbackFunction,
            jac="2-point",
        )
    else:
        return optimize.minimize(
            f,
            initialParameters,
            bounds=bounds,
            method=method,
            options=options,
            callback=minimizerCallbackFunction,
        )


def callSciPyGlobalOptimization(f: Callable, bounds: Sequence, method: str, options: dict):
    if method == "differential_evolution":
        return optimize.differential_evolution(
            f, bounds=bounds, callback=differentialEvolutionCallbackFunction, **options
        )
    elif method == "dual_annealing":
        return optimize.dual_annealing(f, bounds, callback=dualAnnealingCallbackFunction, **options)

    elif method == "brute":
        res = optimize.OptimizeResult()
        res.x = optimize.brute(f, bounds, **options)
        return res

    elif method == "shgo":
        return optimize.shgo(f, bounds, callback=minimizerCallbackFunction, **options)
    else:
        raise Exception("global optimization method {:} not available!".format(method))


def minimizerCallbackFunction(x: np.ndarray, *args):
    printLine()
    infoMessage("current parameters ...")
    for i, val in enumerate(x):
        message(" -->", Identification.active_identifications[i].name, "= {:e}".format(val))
    printLine()


def differentialEvolutionCallbackFunction(x: np.ndarray, convergence=0):
    printLine()
    infoMessage("current parameters ...")
    for i, val in enumerate(x):
        message(" -->", Identification.active_identifications[i].name, "= {:e}".format(val))
    printLine()


def dualAnnealingCallbackFunction(x: np.ndarray, f: float, context: int):
    printLine()
    infoMessage("f = {:}".format(f))
    infoMessage("current parameters ...")
    for i, val in enumerate(x):
        message(" -->", Identification.active_identifications[i].name, "= {:e}".format(val))
    printLine()
