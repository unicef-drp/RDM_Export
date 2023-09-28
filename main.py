"""
This script is used to read from the SDMX DW UNICEF database and RDM
in order to populate a Solr index that can be used to answer questions like:
how many children are starving in a country?
"""
import rdm.RDMQueries as rdmQ
import pandas as pd
from time import sleep
from progress.bar import Bar


def main():
    export_public_indicators()


def export_public_indicators():
    all_indicators = []
    codes = rdmQ.query_all_indicators()
    with Bar("Downloading indicators from RDM...", max=len(codes)) as bar:
        for code in codes:
            indicator = rdmQ.query_indicator_by_helix_code(code)
            all_indicators.append(indicator)
            bar.next()

    # Step 1: Convert list of objects to list of lists
    lst = [
        [
            x.helix_code,
            x.sector,
            x.domain,
            x.subdomain,
            x.ownerAgency,
            x.name,
            x.ALT_NAME,
            x.definition,
            x.numdefinition,
            x.dendefinition,
            x.ADD_DET,
            x.POP_AGGR,
            x.METH_AGGR,
            x.collectionMechanism,
            x.spArea,
            x.spStatement,
            x.classifications,
            x.tags,
            x.itype,
        ]
        for x in all_indicators
    ]
    # adding header
    headerList = [
        "helix_code",
        "sector",
        "domain",
        "subdomain",
        "ownerAgency",
        "name",
        "alt_name",
        "definition",
        "num_definition",
        "den_definition",
        "additional_details",
        "Population_used_for_aggregation",
        "Aggregation_Method",
        "Collection_Process",
        "Strategic_Plan_Goal_Area",
        "Strategic_Plan_Statement",
        "classifications",
        "tags",
        "type",
    ]

    # Step 2: Convert list of lists to CSV
    df = pd.DataFrame(lst)
    df.to_csv("indicators.csv", index=False, header=headerList)


def export_countries():
    # TO BE ADDED
    # rdm.RDMQueries already contains the code to read countries and regions from RDM
    print()


if __name__ == "__main__":
    # calling main function
    main()
