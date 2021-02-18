from scipy.optimize import minimize, Bounds
import numpy as np
import time

from .identification import Identification
from .simulation import Simulation
from .journal import *


def runOptimization( config ):
    
    printSepline() 
    message( " collecting parameters to identify ..." )  
    printLine() 
    
    initialX = []
    lb = []
    ub = []
    
    if "identification" in config:
        for name in config["identification"]:
            # skip inactive identifications
            if "active" in config["identification"][name].keys():
                if config["identification"][name]["active"] == False:
                    message( "  -->  ", name, "(inactive)" ) 
                    continue

            ide = Identification( name, config["identification"][name] )
            initialX.append( ide.start ) 
            lb.append( ide.min ) 
            ub.append( ide.max )

            message( " " +  name + " (active) " )
            message( "   start=" + str( ide.start ) ) 
            message( "     min=" + str( ide.min ) )
            message( "     max=" + str( ide.max ) ) 
            printLine() 
    else:
        message( " no parameter(s) for identification found" )
        exit()
    
    message( " found "+ 
            str( len(Identification.all_identifications) ) +
            " active parameter(s) to identify" ) 
   
    printSepline()
    message( " collecting simulations ..." )
    printLine()


    if "simulations" in config:
        for name in config["simulations"]:
            # skip inactive simulations
            if "active" in config["simulations"][name].keys():
                if config["simulations"][name]["active"] == False:
                    message( "  -->  " + name + " (inactive)" ) 
                    continue
            
            message( "  -->  " + name + " (active)" ) 
            Simulation( name, config["simulations"][name] )
    
    else:
        message( " no simulations found" )
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
   
    printSepline()
    message( " call scipy minimize function ..." )
    message( " ... " )
 
    # execute optimization
    tic = time.time()
    res = minimize(     getResidualForMultipleSimulations, 
                        initialX, 
                        args = ( config ),
                        bounds = Bounds(lb,ub),
                        method=method,
                        options = options )  
    toc = time.time()
    
    printSepline()
    message( " time in minimize function: " + str( round( toc - tic, 4 ) ) + " seconds" )
    

    printSepline()
    message( " write optimal parameters to file ... " )
    # write results to file
    with open( "optimalParameters.txt", "w+") as f:
        for x, ide in zip( res.x, Identification.all_identifications):
            f.write( str(x) + "\t#" + ide.name + "\n" )
            message(  "   {:4.4e}".format( x ) + " " + ide.name ) 
    
    printLine()
    message( " plot results ... " )
    # plot results
    for sim in Simulation.all_simulations:
        sim.plotResults()
    printSepline()

    return res


def getResidualForMultipleSimulations( params, config ):
    
    yErr = np.array( [ ] )
    
    # create residual vector for all simulations
    for sim in Simulation.all_simulations:
        yErr = np.append( yErr, sim.computeResidual( params, config) )
   
    residual = np.linalg.norm( yErr )

    return residual



        




    
