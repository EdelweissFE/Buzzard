import numpy as np

class Material:


    def __init__( self, inputstring ):

        
        split = inputstring.split("," )
        
        matProps = []
        
        for s in split:

            if 'name=' in s.lower():
                self.name = s.split("=")[1]

            elif 'id=' in s.lower():
                self.id = s.split("=")[1]
            else:
                try:
                    matProps.append( float( s ) )
                except:
                    pass

        self.headerString = "*material,name=" + self.name + ",id=" + self.id + "\n"
        self.matProps = np.array( matProps )


