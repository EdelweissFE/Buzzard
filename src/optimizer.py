from scipy.optimize import minimize, Bounds
import numpy as np
import os

def runOptimization( inputDict ):
    
    mat = inputDict["*material"][0]

    # collect all materialparameters to identify
    xIndizes = []
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

    
    initialX = np.array([mat.matProps[i] for i in xIndizes])
    
    print( "initialX = ", initialX )

    res = minimize( getResidualForMultipleSimulations, 
                        initialX, 
                        args = ( inputDict, xIndizes ),
                        bounds = Bounds(lb,ub) ) 

    return res


def getResidualForMultipleSimulations( matParams, inputDict, xIndizes ):
    
    res = 0

    for sim in inputDict['*simulation']:

        res += sim.computeResidual( matParams, inputDict, xIndizes )
    
    print( "||R|| = {:e} ".format( res ) ) 

    return res
