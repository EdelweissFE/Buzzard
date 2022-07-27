from textwrap import wrap

from rich import print

maxCharCentered = 70
maxCharJustified = 68


def printHeader():
    printSepline()
    printCenteredLine("BUZZARD")
    printCenteredLine("")
    printCenteredLine("-- MaterialModelingToolbox --")
    printCenteredLine("github.com/MAteRialMOdelingToolbox")
    printCenteredLine("")
    printSepline()


def infoMessage(*args):
    message(*("INFO:", *args))


def errorMessage(*args):
    message(*("ERROR:", *args))


def message(*args):
    if args:
        string = str(args[0])
        for arg in args[1:]:
            string += " " + str(arg)
        if len(string) < maxCharJustified:
            printJustifiedLine(string)
        else:
            stringList = wrap(string, maxCharJustified - 3)
            printJustifiedLine(stringList[0])
            for string in stringList[1:]:
                printJustifiedLine("..." + string)
    else:
        printJustifiedLine(" ")


def printSepline():
    printCenteredLine(maxCharCentered * "=")


def printLine():
    printCenteredLine(maxCharCentered * "-")


def printCenteredLine(string):
    print("|{:^{}s}|".format(string, maxCharCentered))


def printJustifiedLine(string):
    print("| {:<{}s} |".format(string, maxCharJustified))
