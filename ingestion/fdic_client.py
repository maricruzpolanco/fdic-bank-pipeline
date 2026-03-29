import requests
from requests.exceptions import RequestException, HTTPError

base_url = "https://api.fdic.gov/banks/"
endpoints = ['institutions?fields=name,cert,stalp,asset,repdte,active&limit=1000&offset=0&format=json',
             'financials?fields=repdte,cert,asset,dep,lnlsnet,netinc,rbcrwaj&limit=1000&offset=0&format=json', 'failures?fields=name,cert,faildate,savr,restype,cost&limit=500&format=json']


def fetch_fdic_data(endpoint, fields, filters=None, limit=1000):

    for endpoint in endpoints:
        url = base_url + endpoint
        all_records = []
        offset = 0

        while True:
            params = {
                "fields": fields,
                "limit": limit,
                "offset": offset,
                "format": "json",
                "download": "false"
            }
            if filters:
                params["filters"] = filters

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()

            except RequestsException as e:
                print(f"There was an issue with your request: {e}")
            except HTTPError as e:
                print(f"HTTP error occurred: {e}")

            data = response.json()
            records = data.get("data", [])

            if not records:
                break

            all_records.extend(records)
            offset += limit

            print(f"Fetched {len(all_records)} records from {endpoint}...")

        return all_records

# endpoint_url = "https://api.fdic.gov/banks/institutions?fields=name,cert,stalp,asset,repdte,active&limit=1000&offset=0&format=json"
# response = requests.get(endpoint_url)
# response_json = response.json()
# print(response['name'])


for endpoint in endpoints:
    url = base_url + endpoint
    response = requests.get(url)
    response_dict = response.json()
    print(response_dict)
