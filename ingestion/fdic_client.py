"""
fdic_client.py

Fetches bank data from the FDIC BankFind Suite API
(https://banks.data.fdic.gov/docs/) for three endpoints:
institutions, financials, and failures.

Handles pagination automatically and returns all records
as a dictionary keyed by endpoint name.
"""

import requests
from requests.exceptions import RequestException, HTTPError
import json
import logging


url = "https://api.fdic.gov/banks/"

# Each endpoint definition includes the query parameters sent with every request.
# 'offset' is reset to 0 before each paginated fetch and incremented per page.
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
            # Restrict financials to a five-year window
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
    """Fetch all records from each FDIC API endpoint using pagination.

    Iterates over the globally defined ``endpoints`` dictionary. For each
    endpoint, pages through the API results (using ``limit`` / ``offset``)
    until all records have been collected.

    Returns:
        dict: A dictionary whose keys are endpoint names
              (``"institutions"``, ``"financials"``, ``"failures"``) and
              whose values are lists of record dicts returned by the API.

    Raises:
        requests.exceptions.HTTPError: Re-raised if the API returns a
            non-2xx status code.
        Exception: Any unexpected error during the HTTP request is printed
            and the loop continues to the next page attempt.
    """

    all_data = {}

    for endpoint, endpoint_info in endpoints.items():

        all_records = []

        # Reset pagination offset at the start of each endpoint's fetch
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

                # 'meta.total' tells us the full record count across all pages
                total_record_count = data["meta"]["total"]
                records = data.get("data", [])

                # Each item in 'data' is a wrapper object; the actual record
                # fields live one level deeper under the 'data' key
                all_records.extend([record['data'] for record in records])

                logging.info(
                    f"Fetched {len(all_records)} records from {endpoint}")

                # Stop paginating once we have collected every available record
                if len(all_records) >= total_record_count:
                    break

                # Advance the offset by one full page for the next request
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
