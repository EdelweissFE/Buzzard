class Identification:

    all_identifications = []


    def __init__ ( self, name, config ):

        self.name = name

        self.type= config["type"]
        self.identificator = config["id"]

        self.idx = config["idx"]
        self.start = config["start"]
        self.min = config["min"]
        self.max = config["max"]

        Identification.all_identifications.append( self )
