from scipy.optimize import minimize, Bounds
from optimparallel import minimize_parallel
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import time

from .identification import Identification
from .simulation import Simulation
from .journal import message, infoMessage, printSepline, printLine
from .plotters import *


def runOptimization(config, args):

    method, options = getScipySettings(config)

    initialX, lowerBounds, upperBounds = collectIdentificationsFromConfig(config)

    collectSimulationsFromConfig(config)

    printSepline()
    message(" call scipy minimize function ...")
    message(" ... ")

    # execute optimization
    tic = time.time()

    if args.parallel > 1:

        res = minimize_parallel(
            getResidualForMultipleSimulations,
            initialX,
            args=(args),
            bounds=Bounds(lowerBounds, upperBounds),
            options=options,
            callback=minimizerCallbackFunction,
        )
    else:
        res = minimize(
            getResidualForMultipleSimulations,
            initialX,
            args=(args),
            bounds=Bounds(lowerBounds, upperBounds),
            method=method,
            options=options,
            callback=minimizerCallbackFunction,
        )

    toc = time.time()

    printSepline()
    message(" time in minimize function: " + str(round(toc - tic, 4)) + " seconds")

    printSepline()
    message(" write optimal parameters to file ... ")
    # write results to file
    with open("optimalParameters.txt", "w+") as f:
        for x, ide in zip(res.x, Identification.active_identifications):
            f.write(str(x) + "\t#" + ide.name + "\n")
            message("   {:4.4e}".format(x) + " " + ide.name)

    if args.createPlots:
        printLine()
        message(" plot results ... ")
        plotOptimizationResults(initialX, res.x)

    printSepline()

    return res


def getScipySettings(config):

    method = None
    options = {"disp": True}

    if "scipysettings" in config:
        if "method" in config["scipysettings"]:
            method = config["scipysettings"]["method"]
        if "options" in config["scipysettings"]:
            options = config["scipysettings"]["options"]

    return method, options


def collectIdentificationsFromConfig(config):

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
                ide.active = True
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
        raise Exception("no parameter(s) for identification found")

    message(
        " found "
        + str(len(Identification.active_identifications))
        + " active parameter(s) to identify"
    )

    return initialX, lb, ub


def collectSimulationsFromConfig(config):

    printSepline()
    message(" collecting simulations ...")
    printLine()

    if "simulations" in config:
        for name in config["simulations"]:
            # skip inactive simulations
            if "active" in config["simulations"][name].keys():
                if config["simulations"][name]["active"] == False:
                    message("  -->  " + name + " (inactive)")
                    continue

            message("  -->  " + name + " (active)")
            Simulation(name, config["simulations"][name])

    else:
        message(" no simulations found")
        exit()

    printLine()
    message(" found " + str(len(Simulation.all_simulations)) + " active simulations(s)")


def getResidualForMultipleSimulations(params, args):

    yErr = np.array([])

    if args.parallel in [1, 3]:
        nSim = len(Simulation.all_simulations)
        with ProcessPoolExecutor(max_workers=nSim) as executor:
            future_res = {
                executor.submit(sim.computeResidual, params): sim
                for sim in Simulation.all_simulations
            }

            for future in as_completed(future_res):
                yErr = np.append(yErr, future.result())

    else:
        # create residual vector for all simulations
        for sim in Simulation.all_simulations:
            yErr = np.append(yErr, sim.computeResidual(params))

    residual = np.linalg.norm(yErr)

    return residual


def minimizerCallbackFunction(x, *args):

    printLine()
    infoMessage("current parameters ...")
    for i, val in enumerate(x):
        message(" -->", Identification.active_identifications[i].name + "=" + str(val))
    printLine()
