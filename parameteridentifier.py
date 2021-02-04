import argparse

from src.reader import inputReader
from src.optimizer import runOptimization



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            description='A tool for optimizing (material) parameters for multiple finite element simulations')
    
    parser.add_argument('file', type=str,  nargs = 1, )    
    args=parser.parse_args()
    
    
    inp = inputReader( args.file[0] )
    
    print( 50*"-" )
    opt = runOptimization( inp )
    
    print( 50*"-" )
    print( opt )
