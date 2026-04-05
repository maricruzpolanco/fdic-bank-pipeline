import json
from datetime import datetime
import pytz
import boto3
import logging
import botocore
from dotenv import load_dotenv
import os


load_dotenv()


logging.basicConfig(level=logging.INFO)


def s3_uploader(all_data):

    bucket = "fdic-bank-pipeline-raw"

    est = pytz.timezone('US/Eastern')
    current_date = datetime.now(est).date()
    upload_date = current_date.strftime("%Y/%m/%d")

    try:

        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )

        logging.info("Connection was successful.")
        print()

    except botocore.exceptions.NoCredentialsError:
        logging.error("No AWS credentials found.")
        raise
    except botocore.exceptions.PartialCredentialsError:
        logging.error("Incomplete AWS credentials. Check your .env file.")
        raise
    except Exception as e:
        logging.error(f"Unexpected error creating s3 client: {e}")
        raise

    for key in all_data:

        s3_key = f"{key}/{upload_date}/{key}_raw.json"

        record = all_data[key]
        record_json = json.dumps(record)

        logging.info(f"Uploading data to {key}...")

        try:

            s3.put_object(
                Bucket=bucket,
                Key=s3_key,
                Body=record_json
            )

            logging.info(
                f"File '{s3_key}' was successfully uploaded to '{bucket}' s3 bucket.")
            print()

        except botocore.exceptions.ClientError as error:
            logging.error(f"File '{s3_key}' failed to upload: {error}")
        except Exception as e:
            logging.error(f"Unexpected error loading '{s3_key}': {e}")
            raise
