# from fdic_client import fetch_fdic_data
import json
from datetime import datetime
import pytz
import boto3
import logging
from dotenv import load_dotenv
import os


with open('all_data.json', 'r') as file:
    all_data = json.load(file)

# all_data = fetch_fdic_data()

load_dotenv()


def s3_uploader(all_data):

    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

    est = pytz.timezone('US/Eastern')
    current_date = datetime.now(est).date()
    upload_date = current_date.strftime("%Y/%m/%d")

    for key in all_data:

        record = all_data[key]
        record_json = json.dumps(record)

        s3.put_object(
            Bucket="fdic-bank-pipeline-raw",
            Key=f"{key}/{upload_date}/{key}_raw.json",
            Body=record_json
        )


s3_uploader(all_data)
