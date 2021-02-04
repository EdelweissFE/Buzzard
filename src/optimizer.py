from scipy.optimize import minimize, Bounds
import numpy as np
import os

from .tools import getDictFromString

def runOptimization( inputDict ):
    
    # collect all materialparameters to identify
    xIndizes = []
    initialX = []
    lb = []
    ub = []
    
    if "*identify" in inputDict.keys():
        
        for ide in inputDict["*identify"]:

            d = getDictFromString( ide )
            
            try:
                xIndizes.append( int( d["parameter"] ) )
                initialX.append( d["initial"] )
                lb.append( d["lowerbound"] )
                ub.append( d["upperbound"] )
            except Exception as ex:
                print(" The following excetion occured during indetify collection:\n ",
                        ex )
                exit()
                

    else:
        print( "no parameters given to identify ..." ) 
        exit()
        
    
    customOptions = { "disp": True }
    method = None

    if "*scipyoptions" in inputDict.keys():
        customOptions = getDictFromString( inputDict["*scipyoptions"][0] )
    
        if "method" in customOptions:
            method = customOptions["method"]
            customOptions.pop( "method" )

        if not "disp" in customOptions:
            customOptions["disp"] = True
               
        if not "verbose" in customOptions:
            customOptions["verbose"] = 2

    res = minimize(     getResidualForMultipleSimulations, 
                        initialX, 
                        args = ( inputDict, xIndizes ),
                        bounds = Bounds(lb,ub),
                        method=method,
                        options = customOptions ) 

    return res


def getResidualForMultipleSimulations( X, inputDict, xIndizes ):
    
    yErr = np.array( [ ] )

    for sim in inputDict['*simulation']:

        yErr = np.append( yErr, sim.computeResidual( X, inputDict, xIndizes ) )
    
    residual = np.linalg.norm( yErr )

    return residual



        




    
