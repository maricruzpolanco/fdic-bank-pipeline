import requests
from requests.exceptions import RequestException, HTTPError
import json
import logging
import pprint as pp


base_url = "https://api.fdic.gov/banks/"

endpoints = {
    "institutions": {
        "fields": ["name", "cert", "stalp", "asset", "repdte", "active"],
        "params": {
            "limit": 500,
            "offset": 0,
        }
    },
    "financials": {
        "fields": ["repdte", "cert", "asset", "dep", "lnlsnet", "netinc", "rbcrwaj"],
        "params": {
            "limit": 500,
            "offset": 0,
            "filter": "REPDTE:[2020-01-01 TO 2024-12-31]"
        }
    },
    "failures": {
        "fields": ["name", "cert", "faildate", "savr", "restype", "cost"],
        "params": {
            "limit": 500,
            "offset": 0,
        }
    }
}

# pp.pprint(endpoints)


def fetch_fdic_data():

    for endpoint, endpoint_info in endpoints.items():

        fields_list = endpoint_info["fields"]
        fields = ','.join([str(element) for element in fields_list])
        limit = endpoint_info["params"]["limit"]
        if endpoint_info["params"]["filter"]:
            filters = endpoint_info["params"]["filter"]
        url = f"{base_url}{endpoint}?fields={fields}&limit={limit}&offset=0&format=json&filters"
        print(url)


fetch_fdic_data()
