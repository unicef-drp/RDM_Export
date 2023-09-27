# A Region with info extracted from RDM
class Region:

    def __init__(self, CDNCode, names):
        self.CDNCode = CDNCode
        self.names = names
        self.collection = ""
        self.series = ""
        self.countryISOs = []
