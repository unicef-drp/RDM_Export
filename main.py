"""
This script is used to read from the SDMX DW UNICEF database and RDM
in order to populate a Solr index that can be used to answer questions like:
how many children are starving in a country?
"""
import argparse
import rdm.RDMQueries as rdmQ


# on Linux, use htop to monitor memory usage
def main():
    codes = rdmQ.query_all_indicators()
    for code in codes:
        indicator = rdmQ.query_indicator_by_helix_code(code)
        print(indicator.domain)
        print(indicator.subdomain)
        break


if __name__ == "__main__":
    # calling main function
    main()
