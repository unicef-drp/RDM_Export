import pysolr
from requests.auth import HTTPBasicAuth

import rdm.RDMQueries as rdmQ
import sdmx.SDMXQueries as sdmxQ


class GeoIndexer:

    def __init__(self, solr_endpoint, solr_username, solr_password, sdmx_endpoint, override):
        self.solr_endpoint = solr_endpoint
        self.solr_username = solr_username
        self.solr_password = solr_password
        self.sdmx_endpoint = sdmx_endpoint
        self.override = override

    # Index countries and regions
    def index_countries_regions(self):
        iso3_to_countries = rdmQ.query_countries()
        regions = rdmQ.query_regions()
        # iso3_to_countries = sdmxQ.query_countries(self.sdmx_endpoint)
        # regions = sdmxQ.query_regions(self.sdmx_endpoint)
        print('[+] Countries&Regions downloaded')
        # connect to Solr
        solr = pysolr.Solr(self.solr_endpoint, always_commit=False,
                           auth=HTTPBasicAuth(self.solr_username, self.solr_password))
        # check if the index must be deleted
        if self.override.lower() == "true":
            solr.delete(q='*:*')
            solr.commit()
        # if the index is not deleted, this is just going to be an update
        # index all countries
        for countryISO in iso3_to_countries:
            solr.add([
                {
                    "id": "c_" + str(countryISO),
                    "type": "country",
                    "code": countryISO,
                    "name": iso3_to_countries[countryISO].names
                }
            ])
        # index all regions
        for region in regions:
            # index only UNICEF reporting and UN regions
            if str(region.CDNCode).upper().startswith("UN_") or \
                    str(region.CDNCode).upper().startswith("EU") or \
                    (str(region.CDNCode).upper().startswith("UNICEF_") and
                     "reporting" in str(region.series).lower()):
                # index only regions with attached a list of countries
                if region.countryISOs and len(region.countryISOs) > 0:
                    solr.add([
                        {
                            "id": "r_" + str(region.CDNCode),
                            "type": "region",
                            "code": region.CDNCode,
                            "name": region.names,
                            "related": region.countryISOs
                        }
                    ])
        solr.commit()
        print('[+] Countries&Regions indexed')
