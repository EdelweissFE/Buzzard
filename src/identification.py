from .journal import message


class Identification:

    all_identifications = []
    active_identifications = []

    def __init__(self, name, config):

        self.name = name

        self.start = config["start"]

        try:
            self.active = config["active"]
        except KeyError:
            self.active = True

        if self.active:
            self.min = config["min"]
            self.max = config["max"]
            Identification.active_identifications.append(self)

        Identification.all_identifications.append(self)
