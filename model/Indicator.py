# An Indicator with info extracted from RDM
class Indicator:
    def __init__(self, helix_code):
        self.rdm_id = None
        self.helix_code = helix_code
        self.tags = []
        self.classifications = []
        self.collectionMechanism = ""

        self.name = ""
        self.definition = ""
        self.numdefinition = ""
        self.dendefinition = ""
        self.ADD_DET = ""
        self.POP_AGGR = ""
        self.METH_AGGR = ""

        self.sector = ""
        self.domain = ""
        self.subdomain = ""
