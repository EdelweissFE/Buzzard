import argparse

from src.reader import readConfigFromJson
from src.optimizer import runOptimization



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            description='A tool for optimizing (material) parameters for multiple finite element simulations')
    
    parser.add_argument('file', type=str,  nargs = 1, )    
    args=parser.parse_args()
    
    config = readConfigFromJson( args.file[0] )
    
    opt = runOptimization( config )
    
    print( opt )
