import argparse

from src.reader import readConfigFromJson
from src.optimizer import runOptimization
from src.journal import *

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog = "buzzard",
            description="A tool for optimizing (material) parameters simultaneously for multiple finite element simulations")
    
    parser.add_argument('file', type=str,  nargs = 1, )    
    parser.add_argument(    "--parallel", 
                            type=int,
                            default=0,
                            choices= [0, 1, 2, 3],
                            help=" 0: no parallelization (default); 1: parallel execution of simulations; 2:run parallel minimize (L-BGFS method only); 3: combines option 1 and 2 (L-BGFS method only)")    
    parser.add_argument(    "--createPlots", 
                            action="store_true",
                            default=False)    
    
    args=parser.parse_args()
    printHeader()

    message( " reading config from {:}... ".format( args.file[0]) ) 
    config = readConfigFromJson( args.file[0] )

    success = runOptimization( config, args ) 
    
