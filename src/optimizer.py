from scipy.optimize import minimize, Bounds
import numpy as np
import os

from .identification import Identification
from .simulation import Simulation



def runOptimization( config ):
    
    # collect all parameters to identify
    initialX = []
    lb = []
    ub = []
    
    if "identification" in config:

        for ideName in config["identification"]:
            
            ide = Identification( ideName, config["identification"][ideName] )
            

            initialX.append( ide.start ) 
            lb.append( ide.min ) 
            ub.append( ide.max )
    
    else:
        print( "no parameters for identification found" )
        exit()

    
    # collect all simulations
    if "simulations" in config:

        # initialize all simulations
        for name in config["simulations"]:
            
            Simulation( name, config["simulations"][name] )
    else:
        print( "no simulations found" )
        exit()

    # collect settings for scipy 
    method = None
    options = { "disp": True }
    
    if "scipysettings" in config:

        try:
            method = config["scipysettings"]["method"]
        except:
            pass

        try:
            options = config["scipysettings"]["options"]
        except:
            pass
    
    # execute optimization
    res = minimize(     getResidualForMultipleSimulations, 
                        initialX, 
                        args = ( config ),
                        bounds = Bounds(lb,ub),
                        method=method,
                        options = options ) 
    
    # write results to file
    with open( "optimalParameters.txt", "w+") as f:
        for x, ide in zip( res.x, Identification.all_identifications):
            f.write( str(x) + "\t#" + ide.name + "\n" )
            
    return res


def getResidualForMultipleSimulations( params, config ):
    
    yErr = np.array( [ ] )
    
    # create residual vector for all simulations
    for sim in Simulation.all_simulations:
        yErr = np.append( yErr, sim.computeResidual( params, config) )
   
    residual = np.linalg.norm( yErr )

    return residual



        




    
