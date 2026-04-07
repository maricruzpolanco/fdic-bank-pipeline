"""
s3_uploader.py

Uploads FDIC bank data to an AWS S3 bucket.

Each endpoint's records are serialized to JSON and stored under a
date-partitioned key path:
    <endpoint>/<YYYY>/<MM>/<DD>/<endpoint>_raw.json

AWS credentials are read from a .env file via python-dotenv.
"""

import json
from datetime import datetime
import pytz
import boto3
import logging
import botocore
from dotenv import load_dotenv
import os


# Load AWS credentials from the project's .env file into environment variables
load_dotenv()


logging.basicConfig(level=logging.INFO)


def s3_uploader(all_data):
    """Upload each endpoint's records to the raw S3 bucket as a JSON file.

    Creates a boto3 S3 client using credentials from environment variables,
    then iterates over ``all_data`` and uploads each dataset to a
    date-partitioned S3 key so that historical loads are preserved.

    Args:
        all_data (dict): Dictionary of endpoint name -> list of record dicts,
                         as returned by ``fdic_client.fetch_fdic_data()``.

    Raises:
        botocore.exceptions.NoCredentialsError: If no AWS credentials are
            found in the environment.
        botocore.exceptions.PartialCredentialsError: If only part of the
            required AWS credentials are present.
        botocore.exceptions.ClientError: If a specific S3 upload fails
            (error is logged and the loop continues to the next key).
        Exception: Any other unexpected error creating the S3 client is
            re-raised immediately.
    """

    bucket = "fdic-bank-pipeline-raw"

    # Use Eastern time for the partition date so all daily loads are
    # consistently bucketed regardless of where the code runs
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

        # Build the S3 object key using date partitioning for Athena/Glue compatibility
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
            # Log the failure for this key but continue uploading remaining datasets
            logging.error(f"File '{s3_key}' failed to upload: {error}")
        except Exception as e:
            logging.error(f"Unexpected error loading '{s3_key}': {e}")
            raise
