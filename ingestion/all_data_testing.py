from fdic_client import fetch_fdic_data
import json

all_data = fetch_fdic_data()

with open('all_data.json', 'w') as file:
    json.dump(all_data, file, indent=4)
