import numpy as np
import sys

from .identification import Identification

edelweissPath = "/home/ad/constitutiveModelling/EdelweissFE"
sys.path.append( edelweissPath )

import fe
from fe.fecore import finitElementSimulation
from fe.utils.inputfileparser import parseInputFile 


def evaluateEdelweissSimulation( currParams, configDict, simName ):

    simConfig = configDict["simulations"][simName]
    fieldoutputX = simConfig["simX"]
    fieldoutputY = simConfig["simY"]

    # load input file 
    inp = parseInputFile( simConfig["input"] )
    
    # replace material parameters to identify
    i = 0
    for ide in Identification.all_identifications:
        if ide.type == "material":
            for n in range( len( inp["*material"] ) ):
                if inp["*material"][n]["id"] == ide.identificator:
                    inp["*material"][n]["data"][0][ide.idx] = currParams[i]
        
        i += 1

    success, U, P, fieldOutputController = finitElementSimulation( inp, verbose=False )


    if fieldoutputX == fieldoutputY:
        # get time history as x value if only one fieldoutput is given 
        x = np.abs( fieldOutputController.fieldOutputs[fieldoutputX].timeHistory )
        y = fieldOutputController.fieldOutputs[fieldoutputY].result
    else:
        x = np.abs( fieldOutputController.fieldOutputs[fieldoutputX].result )
        y = fieldOutputController.fieldOutputs[fieldoutputY].result


    return x, y


