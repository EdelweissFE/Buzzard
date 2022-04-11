import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from similaritymeasures import frechet_dist, area_between_two_curves, pcm

from .journal import message
from .abaqusUtility import *


class Simulation:

    all_simulations = []

    def __init__(self, name, config):

        self.name = name
        self.type = config["type"]

        if type(config["data"]) == list:
            self.data = np.concatenate(
                tuple([np.loadtxt(d) for d in config["data"]]), axis=0
            )
        else:
            self.data = np.loadtxt(config["data"])

        try:
            self.errorType = config["errorType"]
        except:
            self.errorType = "relative"

        if self.type == "edelweiss":
            from .edelweissUtility import readEdelweissInputfile

            self.inp = readEdelweissInputfile(config["input"])
            self.fieldoutputX = config["simX"]
            self.fieldoutputY = config["simY"]
        elif self.type == "abaqus":
            self.inp = open(config["input"]).read()
            self.postProcessingScript = config["postProcessingScript"]
            self.executeable = config["executeable"]
            self.cpus = config["cpus"]
        Simulation.all_simulations.append(self)

    def run(self, currParams):

        if self.type == "edelweiss":

            from .edelweissUtility import evaluateEdelweissSimulation

            x, y = evaluateEdelweissSimulation(currParams, self)

        elif self.type == "abaqus":

            x, y = evaluateAbaqusSimulation(currParams, self)

        else:
            print("type of simulation not defined")
            exit()

        return x, y

    def computeResidual(self, currParams):

        x, y = self.run(currParams)

        if type(x) is not np.ndarray:
            print("params = ", currParams)
            return np.array([1e12])

        return self.computeErrorVector(x, y)

    def computeErrorVector(self, x, y):

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
                    print(e)

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
            message(" wrong type for error calculation ...")
            exit()

        return yErr

    def interpolateSimulationResults(self, x, y):

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
