import numpy as np
import sys

# load EdelweissFE
edelweissPath = "/home/ad/constitutiveModelling/EdelweissFE"
sys.path.append( edelweissPath )
import fe
from fe.fecore import finitElementSimulation
from fe.utils.inputfileparser import parseInputFile 
from fe.utils.misc import mergeNumpyDataLines

from .identification import Identification

def readEdelweissInputfile( filename ):

    inp = parseInputFile( filename )
    
    # flatten data lines for material data
    for n in range( len( inp["*material"] ) ):
         inp["*material"][n]["data"] = mergeNumpyDataLines( inp["*material"][n]["data"] )

    return inp

def setCurrentParams( currParams, sim ):
    
    i = 0
    for ide in Identification.all_identifications: 
        if ide.type == "material":
            for n in range( len( sim.inp["*material"] ) ):
                if sim.inp["*material"][n]["id"] == ide.identificator:
                    
                    sim.inp["*material"][n]["data"][ide.idx] = currParams[i]
        i += 1

def evaluateEdelweissSimulation( currParams, sim ):

    # replace parameters for the simulation
    setCurrentParams( currParams, sim )

    # execute simulation
    success, U, P, fieldOutputController = finitElementSimulation( sim.inp, verbose=False )
    
    if success:

        if sim.fieldoutputX == sim.fieldoutputY:
            # get time history as x value if only one fieldoutput is given 
            x = np.array( fieldOutputController.fieldOutputs[sim.fieldoutputX].timeHistory )
            y = np.array( fieldOutputController.fieldOutputs[sim.fieldoutputY].result )
        else:
            x = np.array( fieldOutputController.fieldOutputs[sim.fieldoutputX].result )
            y = np.array( fieldOutputController.fieldOutputs[sim.fieldoutputY].result )
    else:
        print( "simulation failed !!!" )
        x = None
        y = None
        
    return x, y


