import requests
from requests.exceptions import RequestException, HTTPError
import json
import logging


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


logging.basicConfig(level=logging.INFO)


def fetch_fdic_data():

    all_data = {}

    for endpoint, endpoint_info in endpoints.items():

        all_records = []

        endpoint_info["params"]["offset"] = 0

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

                response.raise_for_status()
                data = response.json()
                total_record_count = data["meta"]["total"]
                records = data.get("data", [])

                all_records.extend([record['data'] for record in records])

                logging.info(
                    f"Fetched {len(all_records)} records from {endpoint}")
                if len(all_records) >= total_record_count:
                    break

                endpoint_info["params"]["offset"] += endpoint_info["params"]["limit"]

            except HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
            except Exception as e:
                print("An error has occurred with the request:", e)

        logging.info(
            f"Completed fetching {endpoint}: {len(all_records)} total records")

        all_data[endpoint] = all_records

    return all_data


if __name__ == "__main__":
    fetch_fdic_data()
