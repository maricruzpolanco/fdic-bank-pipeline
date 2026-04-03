# from fdic_client import fetch_fdic_data
import json
from datetime import datetime
import pytz


with open('all_data.json', 'r') as file:
    all_data = json.load(file)

# all_data = fetch_fdic_data()

records_list = []


def s3_uploader(all_data):
    est = pytz.timezone('US/Eastern')
    upload_date = datetime.now(est).date()
    print(upload_date)

    for key, value in all_data.items():
        records_list.append({"endpoint": key, "fields": value})
        print(records_list)

    # with open("end.json", "w") as json_file:
    #     json_dump()


s3_uploader(all_data)
