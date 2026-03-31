import requests
from requests.exceptions import RequestException, HTTPError
import json
import logging
import time
import pprint as pp


url = "https://api.fdic.gov/banks/"

endpoints = {
    "institutions": {
        "params": {
            "fields": "NAME,CERT,STALP,ASSET,REPDTE,ACTIVE",
            "limit": 10000,
            "offset": 0,
            "format": "json",
        }
    },
    "financials": {
        "params": {
            "fields": "REPDTE,CERT,ASSET,DEP,LNLSNET,NETINC,RBCRWAJ",
            "limit": 10000,
            "offset": 0,
            "format": "json",
            "filters": "REPDTE:[2020-01-01 TO 2024-12-31]"
        }
    },
    "failures": {
        "params": {
            "fields": "NAME,CERT,FAILDATE,SAVR,RESTYPE,COST",
            "limit": 10000,
            "offset": 0,
            "format": "json"
        }
    }
}

# pp.pprint(endpoints)

logging.basicConfig(level=logging.INFO)


def fetch_fdic_data():

    for endpoint, endpoint_info in endpoints.items():

        all_records = []

        while True:

            try:

                response = requests.get(
                    url + endpoint, params=endpoint_info["params"])
                logging.info(
                    f"Sent API request for {endpoint}: {response.url}")

                if response.status_code == 200:
                    logging.info(f"Request for {endpoint} was successfull")
                else:
                    logging.warning(
                        f"Unexpected status code: {response.status_code}")

                # print(response.base_url)
                response.raise_for_status()
                data = response.json()
                records = data.get("data", [])

                logging.info(
                    f"Fetched {len(all_records)} records from {endpoint}")

                if not records:
                    break

                all_records.extend(records)
                endpoint_info["params"]["offset"] += endpoint_info["params"]["limit"]

                pp.pprint(records)

            except Exception as e:
                print("An error has occurred with the request:", e)

    return all_records


fetch_fdic_data()
