import argparse
import os

from src.reader import readConfig, readConfigFromJson
from src.optimizer import runOptimization
from src.journal import *

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="buzzard",
        description="A tool for optimizing (material) parameters simultaneously for multiple finite element simulations",
    )

    parser.add_argument(
        "file",
        type=str,
        nargs=1,
    )
    parser.add_argument(
        "--parallel",
        type=int,
        default=0,
        choices=[0, 1, 2, 3],
        help=" 0: no parallelization (default); 1: parallel execution of simulations; 2:run parallel minimize (L-BGFS method only); 3: combines option 1 and 2 (L-BGFS method only)",
    )
    parser.add_argument("--createPlots", action="store_true", default=False)

    args = parser.parse_args()
    printHeader()

    configFile = args.file[0]
    root, ext = os.path.splitext(configFile)
    if ext == ".py":
        config = readConfig(configFile)
    elif ext == ".json":
        config = readConfigFromJson(configFile)
    else:
        raise Exception("File type of config file must be .py or .json")

    # set environment variables
    if "env_variables" in config.keys():
        for var, value in config["env_variables"].items():
            os.environ[var] = value

    success = runOptimization(config, args)
