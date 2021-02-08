import numpy as np
import sys

# load EdelweissFE
edelweissPath = "/home/ad/constitutiveModelling/EdelweissFE"
sys.path.append( edelweissPath )
import fe
from fe.fecore import finitElementSimulation
from fe.utils.inputfileparser import parseInputFile 


from .identification import Identification


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

                    j = 0
                    offset = 0
                    for j in range( len( inp["*material"][n]["id"] ) ):
                        if ide.idx - offset < len( inp["*material"][n]["data"][j] ):
                            inp["*material"][n]["data"][j][ide.idx - offset ] = currParams[i]
                            break
                        else:
                            offset += len( inp["*material"][n]["data"][j] )
                    
        i += 1
    
    # execute simulation
    success, U, P, fieldOutputController = finitElementSimulation( inp, verbose=False )


    if fieldoutputX == fieldoutputY:
        # get time history as x value if only one fieldoutput is given 
        x = np.abs( fieldOutputController.fieldOutputs[fieldoutputX].timeHistory )
        y = fieldOutputController.fieldOutputs[fieldoutputY].result
    else:
        x = np.abs( fieldOutputController.fieldOutputs[fieldoutputX].result )
        y = fieldOutputController.fieldOutputs[fieldoutputY].result


    return x, y


