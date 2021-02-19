import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

from .edelweissUtility import *

class Simulation:
    
    all_simulations = []

    def __init__( self, name, config ):

            
        self.name = name
        self.type = config["type"]
        self.data = np.loadtxt( config["data"] )
        
        if self.type == "edelweiss":
            self.inp = readEdelweissInputfile( config["input"] )
            self.fieldoutputX = config["simX"] 
            self.fieldoutputY = config["simY"] 

        Simulation.all_simulations.append( self )

    def run( self, currParams):
         
        if self.type == "edelweiss":
            x, y = evaluateEdelweissSimulation( currParams, self ) 
            
        else:
            print( "type of simulation not defined" )
            exit()

        return x, y

    def computeResidual( self, currParams ):
         
       
        x, y = self.run( currParams )

        if type(x) is not np.ndarray:
            print("params = ", currParams )
            return np.array( [1e12] )

        xlist = [x[0]]
        ylist = [y[0]]

        if x[0] > x[-1]:
            for i, val in enumerate(x[1:]):
                if x[i+1] < x[i]:
                    xlist.append(float(val))
                    ylist.append(float(y[i+1]))

            xySim = interp1d(   xlist[::-1] , ylist[::-1] )
        else:
            for i, val in enumerate(x[1:]):
                if x[i+1] > x[i]:
                    xlist.append(float(val))
                    ylist.append(float(y[i+1]))

            xySim= interp1d(   xlist , ylist )

        # compute relative error vector
        yErr = np.array([])
        for i in range( len( self.data[:,1] ) ):
            if self.data[i,1] == 0:
                continue

            try:
                yErr = np.append( yErr,
                   ( self.data[i,1] - xySim(  self.data[i,0]  ) ) / self.data[i,1] )
            except:
                pass

        return yErr
    


