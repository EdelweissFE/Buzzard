import json


def readConfigFromJson( jsonfile ):
    with open( jsonfile, "r" ) as j:
        data = json.load( j )

    return data



