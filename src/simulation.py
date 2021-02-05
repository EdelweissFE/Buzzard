import numpy as np
import os
from scipy.interpolate import interp1d
from random import random


from .tools import getDictFromString

from .edelweissUtility import *


edelweissExecuteable = "python /home/ad/constitutiveModelling/EdelweissFE/edelweiss.py"


class Simulation:
    
    all_simulations = []

    def __init__( self, name, config ):

            
        self.name = name
        self.type = config["type"]
        self.xy = np.loadtxt( config["data"] )

        Simulation.all_simulations.append( self )


    def computeResidual( self, currParams, configDict ):
         
        if self.type == "edelweiss":

            x, y = evaluateEdelweissSimulation( currParams, configDict, self.name ) 
            
        else:
            print( "type of simulation not defined" )
            exit()
       
        
        xySim = interp1d( x, y )

        yErr = np.array( 
                    [   self.xy[i,1] - xySim( abs( self.xy[i,0] ) ) 
                        for i in range( len( self.xy[:,0] ))  ] )

        return yErr / max( np.abs( self.xy[:,1] ) )
