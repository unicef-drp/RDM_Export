# An Indicator with info extracted from RDM
class Indicator:
    def __init__(self, helix_code):
        self.rdm_id = None
        self.helix_code = helix_code

        self.sector = ""
        self.domain = ""
        self.subdomain = ""
        self.ownerAgency = ""

        self.name = ""
        self.ALT_NAME = ""
        self.definition = ""
        self.numdefinition = ""
        self.dendefinition = ""
        self.ADD_DET = ""
        self.POP_AGGR = ""
        self.METH_AGGR = ""

        self.collectionMechanism = ""
        self.spArea = ""
        self.spStatement = ""

        self.classifications = []
        self.tags = []
        self.itype = ""
