import os
import sys
import json
from .journal import message

def readConfigFromJson(jsonfile):
    message("reading config from {:}... ".format(jsonfile))

    with open(jsonfile, "r") as j:
        data = json.load(j)

    return data


def readConfig(configFile):
    message("reading config from {:}... ".format(configFile))

    (head, tail) = os.path.split(configFile)
    sys.path.append(head)
    (root, ext) = os.path.splitext(tail)
    config = __import__(root).config

    return config
