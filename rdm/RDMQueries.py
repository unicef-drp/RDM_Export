import requests
import json

from model.Country import Country
from model.Indicator import Indicator

# Query RDM indicator by helix code
from model.Region import Region


def query_all_indicators():
    api_base_path = "https://rdmapi.unicef.org/api/indicators/"
    codes = []
    response = requests.get(api_base_path)
    if response.status_code == 200:
        json_response = response.json()
        for indicator in json_response:
            codes.append(indicator["helixCode"])
    return codes


def query_indicator_by_helix_code(helix_code):
    sectors = {}
    sectors_paths = "https://rdmapi.unicef.org/api/sectors"
    response = requests.get(sectors_paths)
    if response.status_code == 200:
        json_response = response.json()
        for sector in json_response:
            sectors[sector["sectorId"]] = sector["name"]

    domains = {}
    domain_paths = "https://rdmapi.unicef.org/api/sectors/domains"
    response = requests.get(domain_paths)
    if response.status_code == 200:
        json_response = response.json()
        for domain in json_response:
            domains[domain["domainId"]] = domain["name"]

    subdomains = {}
    sd_paths = "https://rdmapi.unicef.org/api/sectors/subdomains"
    response = requests.get(sd_paths)
    if response.status_code == 200:
        json_response = response.json()
        for sd in json_response:
            subdomains[sd["subdomainId"]] = sd["name"]

    api_base_path = "https://rdmapi.unicef.org/api/indicators/"
    path = api_base_path + helix_code
    response = requests.get(path)
    if response.status_code == 200:
        json_response = json.loads(response.text)
        indicator = Indicator(helix_code)
        if type(json_response) is dict and bool(json_response):
            if "indicatorId" in json_response:
                indicator.rdm_id = json_response["indicatorId"]
            if "sector" in json_response:
                jsector = json_response["sector"]
                indicator.sector = sectors[int(jsector)]
            if "domain" in json_response:
                jdomain = json_response["domain"]
                indicator.domain = domains[int(jdomain)]
            if "subdomain" in json_response:
                jsubdomain = json_response["subdomain"]
                if jsubdomain != "":
                    indicator.subdomain = subdomains[int(jsubdomain)]
            if "classifications" in json_response:
                # list of dictionaries
                classifications = json_response["classifications"]
                if type(classifications) is list and len(classifications) > 0:
                    for classification in classifications:
                        if (
                            type(classification) is dict
                            and bool(classification)
                            and "name" in classification
                        ):
                            value = classification["value"]
                            if value == "true":
                                indicator.classifications.append(classification["name"])
            if "tags" in json_response:
                tags = json_response["tags"]  # list of dictionaries
                if type(tags) is list and len(tags) > 0:
                    for tag in tags:
                        if type(tag) is dict and bool(tag) and "tagName" in tag:
                            if len(tag) > 0:
                                indicator.tags.append(tag)
            if "collectionMechanism" in json_response:
                collectionMechanism = json_response["collectionMechanism"]
                indicator.collectionMechanism = collectionMechanism["name"]
            if "strategicPlanArea" in json_response:
                strategicPlanArea = json_response["strategicPlanArea"]
                indicator.spArea = strategicPlanArea["name"]
            if "strategicPlanStatement" in json_response:
                strategicPlanStatement = json_response["strategicPlanStatement"]
                indicator.spStatement = strategicPlanStatement["statement"]
            if "type" in json_response:
                itype = json_response["type"]
                indicator.itype = itype["typeName"]
            if "ownerAgency" in json_response:
                ownerAgency = json_response["ownerAgency"]
                indicator.ownerAgency = ownerAgency["organization"]
            if "attributes" in json_response:
                attributes = json_response["attributes"]  # list of dictionary
                if type(attributes) is list and len(attributes) > 0:
                    for attr in attributes:
                        if (
                            type(attr) is dict
                            and bool(attr)
                            and "attributeName" in attr
                            and "language" in attr
                            and "value" in attr
                        ):
                            # only english attributes
                            if attr["language"].lower() == "english":
                                if (
                                    attr["attributeName"].lower()
                                    == "indicator name".lower()
                                ):
                                    indicator.name = (
                                        attr["value"]
                                        .replace("\n", " ")
                                        .replace("\t", " ")
                                        .replace("\r", " ")
                                    )
                                if (
                                    attr["attributeName"].lower()
                                    == "indicator definition".lower()
                                ):
                                    indicator.definition = attr["value"]
                                if (
                                    attr["attributeCode"].lower()
                                    == "NUM_DEFINITION".lower()
                                ):
                                    indicator.numdefinition = attr["value"]
                                if (
                                    attr["attributeCode"].lower()
                                    == "DEN_DEFINITION".lower()
                                ):
                                    indicator.dendefinition = (
                                        attr["value"]
                                        .replace("\n", " ")
                                        .replace("\t", " ")
                                        .replace("\r", " ")
                                    )
                                if attr["attributeCode"].lower() == "POP_AGGR".lower():
                                    indicator.POP_AGGR = (
                                        attr["value"]
                                        .replace("\n", " ")
                                        .replace("\t", " ")
                                        .replace("\r", " ")
                                    )
                                if attr["attributeCode"].lower() == "METH_AGGR".lower():
                                    indicator.METH_AGGR = (
                                        attr["value"]
                                        .replace("\n", " ")
                                        .replace("\t", " ")
                                        .replace("\r", " ")
                                    )
                                if attr["attributeCode"].lower() == "ADD_DET".lower():
                                    indicator.ADD_DET = (
                                        attr["value"]
                                        .replace("\n", " ")
                                        .replace("\t", " ")
                                        .replace("\r", " ")
                                    )
                                if attr["attributeCode"].lower() == "ALT_NAME".lower():
                                    indicator.ALT_NAME = (
                                        attr["value"]
                                        .replace("\n", " ")
                                        .replace("\t", " ")
                                        .replace("\r", " ")
                                    )
            return indicator
    return None


# get all current countries from RDM, returning a dictionary ISO3 -> country
def query_countries():
    result = {}
    path = "https://rdmapi.unicef.org/api/countries/current"
    response = requests.get(path)
    if response.status_code == 200:
        json_response = json.loads(response.text)  # list of dictionaries
        if type(json_response) is list and len(json_response) > 0:
            for country in json_response:
                iso3 = ""
                en_names = []
                ispublished = "true"
                if type(country) is dict and bool(country):
                    if "iso3" in country:
                        iso3 = country["iso3"]
                    if "isPublished" in country:
                        ispublished = country["isPublished"]
                    if "language2Name" in country:
                        # list of dictionary
                        language2name = country["language2Name"]
                        if type(language2name) is list and len(language2name) > 0:
                            for lang in language2name:
                                if (
                                    type(lang) is dict
                                    and bool(lang)
                                    and "languageName" in lang
                                    and "value" in lang
                                ):
                                    # only english langs
                                    if (
                                        lang["languageName"].lower() == "english"
                                        and not lang["value"] in en_names
                                    ):
                                        en_names.append(lang["value"])
                    if len(en_names) > 0 and len(iso3) == 3:
                        result[iso3] = Country(iso3, en_names, ispublished)
    return result


# get all regions from RDM, returning a list
def query_regions():
    result = []
    path = "https://rdmapi.unicef.org/api/regions"
    response = requests.get(path)
    if response.status_code == 200:
        json_response = json.loads(response.text)  # list of dictionaries
        if type(json_response) is list and len(json_response) > 0:
            for region in json_response:
                code = ""
                collection = ""
                series = ""
                en_names = []
                countries = []
                if type(region) is dict and bool(region):
                    if "cndregionalCode" in region:
                        code = region["cndregionalCode"]
                        if code.upper() == "UN_GLOBAL":
                            # this would be the alternate name, but it is dangerous to use it for other regions, it can create conflicts
                            en_names.append("World")
                    if "collection" in region:
                        tmp = region["collection"]
                        if type(tmp) is dict and bool(tmp) and "name" in tmp:
                            collection = tmp["name"]
                    if "series" in region:
                        tmp = region["series"]
                        if type(tmp) is dict and bool(tmp) and "name" in tmp:
                            series = tmp["name"]
                    if "language2Name" in region:
                        # list of dictionary
                        language2name = region["language2Name"]
                        if type(language2name) is list and len(language2name) > 0:
                            for lang in language2name:
                                if (
                                    type(lang) is dict
                                    and bool(lang)
                                    and "languageName" in lang
                                    and "value" in lang
                                ):
                                    # only english langs
                                    if (
                                        lang["languageName"].lower() == "english"
                                        and not lang["value"] in en_names
                                    ):
                                        en_names.append(lang["value"])
                    if "countries" in region:
                        # list of dictionary
                        all_countries = region["countries"]
                        if type(all_countries) is list and len(all_countries) > 0:
                            for country in all_countries:
                                if (
                                    type(country) is dict
                                    and bool(country)
                                    and "countryISO" in country
                                ):
                                    if (
                                        len(country["countryISO"]) > 0
                                        and not country["countryISO"] in countries
                                    ):
                                        countries.append(country["countryISO"])
                    if len(en_names) > 0:
                        region = Region(code, en_names)
                        region.collection = collection
                        region.series = series
                        region.countryISOs = countries
                        result.append(region)
    return result
