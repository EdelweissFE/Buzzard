import numpy as np
import sys
import os
import subprocess
import random as rd

from .identification import Identification

abaqusExecuteable = "abaqus "


def evaluateAbaqusSimulation( currParams, sim ):

    randomFileName = "_temp_" + str( rd.randint(0,1e16) )  

    # create input for current parameters
    paramIDX = 0
    
    data = str( sim.inp )
    for ide in Identification.all_identifications:
            
        if ide.active:
            data = data.replace( ide.name, str( currParams[paramIDX] ) )
            paramIDX += 1
        else:
            data = data.replace( ide.name, str( ide.start ) )
    
    
    with open( randomFileName + ".inp", "w+" ) as n:
        n.write( data )


    # execute simulation
    
    simCommand = abaqusExecuteable
    simCommand += " -j " + randomFileName

    success = runCommandAndCatchError( simCommand )
    
    if success:
        runCommandAndCatchError( " ".join(  abaqusExecuteable, 
                                            "python", 
                                            sim.postrProcessingScript, 
                                            randomFileName + ".odb",
                                            randomFileName + "out" ) )

    
    # remove all generated files
    os.system( "rm {name}*".format(name = randomFileName ) )
        
    return None, None


def runCommandAndCatchError( command ):

    com = [c.replace("'","") for c in command.split(' ')]
    pipe = subprocess.Popen(com, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    
    text = ""
    for i in pipe.communicate():
        text += i.decode( "utf-8" )

    if 'error' in text.lower():
        message( text )
        return False

    else:
        return True
