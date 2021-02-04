from scipy.optimize import minimize, Bounds
import numpy as np
import os

def runOptimization( inputDict ):
    
    # collect all materialparameters to identify
    xIndizes = []
    initialXList = []
    lb = []
    ub = []

    for ide in inputDict["*identify"]:

        split = ide.split(",")
        for s in split:
            if "parameter=" in s.lower():
                xIndizes.append( int( s.split("=")[1] ))

            elif "upperbound=" in s.lower():
                ub.append( float( s.split("=")[1] ))
    
            elif "lowerbound=" in s.lower():
                lb.append( float( s.split("=")[1] ))

            elif "initial=" in s.lower():
                initialXList.append( float( s.split("=")[1] ))
    
    initialX = np.array( initialXList )
    
    print( "initialX = ", initialX )

    res = minimize( getResidualForMultipleSimulations, 
                        initialX, 
                        args = ( inputDict, xIndizes ),
                        bounds = Bounds(lb,ub),
                        method="TNC") 

    return res


def getResidualForMultipleSimulations( X, inputDict, xIndizes ):
    
    res = 0

    for sim in inputDict['*simulation']:

        res += sim.computeResidual( X, inputDict, xIndizes )
    
    print( "||R|| = {:e} ".format( res ) ) 

    return res
