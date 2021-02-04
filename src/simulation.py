import numpy as np
import os
from scipy.interpolate import interp1d

edelweissExecuteable = "python /home/ad/constitutiveModelling/EdelweissFE/edelweiss.py"


class Simulation:


    def __init__( self, inputstring ):

        
        split = inputstring.split("," )

        for s in split:

            if 'type=' in s.lower():
                self.type = s.split("=")[1]

            elif 'input=' in s.lower():
                
                with open( s.split("=")[1], 'r' ) as f:
                    self.input = f.read()


            elif 'outx=' in s.lower():
                self.simX = s.split("=")[1]

            elif 'outy=' in s.lower():
                self.simY = s.split("=")[1]
    
            elif 'xy=' in s.lower():
                self.xy = np.loadtxt( s.split("=")[1] )





    def computeResidual( self, materialParams, inputDict, matIndizes ):
        
        
        
        if self.type == "edelweiss":


            mat = inputDict["*material"][0]
        
            currMatProps = mat.matProps
        
            c = 0
            for i in matIndizes:
                currMatProps[i] = materialParams[c]
                c += 1

            matString = mat.headerString
            c = 0
            for p in currMatProps:
                matString += str(p) +","
                if c == 7:
                    matString += "\n"
                    c = -1
                c += 1
            # write individual inptfile
            with open( "currentInput.inp", "w+") as f:

                f.write( matString )
                f.write( "\n" )
                f.write( self.input )
        
            
            os.system( edelweissExecuteable + " currentInput.inp --quiet " )

            # load x y data from simulation results
            if self.simX == self.simY:
                x = np.abs( np.loadtxt( self.simX )[:,0] )
                y = np.loadtxt( self.simX )[:,1]
            else:
                x = np.abs( np.loadtxt( self.simX )[:,1] )
                y = np.loadtxt( self.simY )[:,1]

            xySim = interp1d( x, y )

            yErr = np.array( 
                    [ abs( self.xy[i,1] - xySim( abs( self.xy[i,0] ) )) 
                        for i in range( len( self.xy[:,0] ))  ] )
        
        else:
            print( "type of simulation not defined" )
            exit()
        
        return np.linalg.norm( yErr ) 
