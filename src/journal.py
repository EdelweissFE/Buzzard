from rich import print


def printHeader():
    printSepline()
    print("|{:^70s}|".format("BUZZARD"))
    print("|{:^70s}|".format(""))
    print("|{:^70s}|".format("-- MaterialModelingToolbox --"))
    print("|{:^70s}|".format("github.com/MAteRialMOdelingToolbox"))
    print("|{:^70s}|".format(""))
    printSepline()


def message(string):
    print("|{:<70s}|".format(string))


def printSepline():
    message(70 * "=")


def printLine():
    message(70 * "-")
