from .journal import message


class Identification:

    all_identifications = []

    def __init__(self, name, config):

        self.name = name

        self.start = config["start"]
        self.min = config["min"]
        self.max = config["max"]

        try:
            self.active = config["active"]
        except KeyError:
            self.active = True

        # additional configuration for edelweiss simulations
        try:
            self.type = config["type"]
            self.identificator = config["id"]
            self.idx = config["idx"]
        except Exception as e:
            message("NOTE: additional keywords for edelweiss simulation not defined")

        Identification.all_identifications.append(self)
