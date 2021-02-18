import argparse

from src.reader import readConfigFromJson
from src.optimizer import runOptimization
from src.journal import *

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            description="A tool for optimizing (material) parameters simultaneously for multiple finite element simulations")
    
    parser.add_argument('file', type=str,  nargs = 1, )    
    args=parser.parse_args()
    
    printHeader()

    message( " reading config from {:}... ".format( args.file[0]) ) 
    config = readConfigFromJson( args.file[0] )

    success = runOptimization( config ) 
    
