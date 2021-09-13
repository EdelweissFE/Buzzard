import numpy as np
import sys
import os
import subprocess
import random as rd

from .identification import Identification
from .journal import message

# abaqusExecuteable = 'singularity exec /home/ad/constitutiveModelling/abaqus-2019-centos-7.simg abaqus'


def evaluateAbaqusSimulation( currParams, sim ):

    randomFileName = '_temp_' + str( rd.randint(0,1e16) )  

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
     
    abaqusExecuteable = sim.executeable
    cpus = sim.cpus
    
    simCommand = ' '.join( [ abaqusExecuteable, '-j', randomFileName, 'interactive', 'cpus='+str(cpus) ] )
    
    success = runCommandAndCatchError( simCommand )
    
    if success:
        runCommandAndCatchError( ' '.join([ abaqusExecuteable, 
                                            'python', 
                                            sim.postProcessingScript, 
                                            randomFileName + '.odb',
                                            randomFileName + '.out' ] ) )
        simdata = np.loadtxt( randomFileName + '.out' )
        x = simdata[:,0]
        y = simdata[:,1]
    else:
        x = None
        y = None
    
    # remove all generated files
    os.system( "rm -r {name}*".format(name = randomFileName ) )
    
    return x, y


def runCommandAndCatchError( command ):

    com = [c.replace("'","") for c in command.split(' ')]
    pipe = subprocess.Popen(com, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

    text = ""
    for i in pipe.communicate():
        text += i.decode( "utf-8" )

    if 'error' in text.lower():
        message( str( com ) )
        message( text )
        return False

    else:
        return True
