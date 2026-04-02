from fdic_client import fetch_fdic_data
import json
from datetime import datetime
import pytz


all_data = fetch_fdic_data()


def s3_uploader(all_data):
    est = pytz.timezone('US/Eastern')
    upload_date = datetime.now(est).date()
    print(upload_date)


s3_uploader(all_data)
