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

        
        if x[0] > x[1]:
            xySim = interp1d(   x[::-1] , y[::-1] )
        else:
            xySim= interp1d(   x , y )
        # compute relative error vector
        yErr = np.array([])
        for i in range( len( self.data[:,1] ) ):
            if self.data[i,1] == 0:
                continue
            yErr = np.append( yErr,
                   ( self.data[i,1] - xySim(  self.data[i,0]  ) ) / self.data[i,1] )
                    

        return yErr
    


