from .simulation import Simulation
from .material import Material


def inputReader( filename ):
    
    keywords = ['*material', '*simulation', '*identify']

    print( "reading input from", filename, "..." )
    
    inp = { keyword: [] for keyword in keywords }
    
    currKey = None
    currInpString = ""

    with open( filename, 'r') as f:

        lines = f.readlines( )
        
        for line in lines:
            if "**" in line:
                continue
            line = line.replace(" ", "")
            if line == "\n":
                continue
            line = line.replace( "\n", ",")
            split = line.split(',')
             
            if currKey is None:
                if split[0] in keywords:
                    currKey = split[0]
                    currInpString = line 

            else:
                
                if split[0] in keywords:
                    # create object for old inputstring
                    obj = createObjectForKeyword( currKey, currInpString )
                    inp[currKey].append( obj )
                    currKey = split[0]
                    currInpString = line

                else:
                    currInpString += line

        
        # create object for old inputstring
        obj = createObjectForKeyword( currKey, currInpString )
        inp[currKey].append( obj )

    return inp


def createObjectForKeyword( keyword, inputstring ):

    if keyword == "*simulation":
        return Simulation( inputstring )
    
    elif keyword == "*material":
        return Material( inputstring )
    
    else:
        return inputstring
