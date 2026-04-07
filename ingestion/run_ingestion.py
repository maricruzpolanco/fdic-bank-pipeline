"""
run_ingestion.py

Entry point for the FDIC bank data ingestion pipeline.

Orchestrates the two pipeline stages in sequence:
  1. fdic_client.fetch_fdic_data  -- pulls records from the FDIC API
  2. s3_uploader.s3_uploader      -- uploads those records to S3

Logging is written to both the console and a local 'app.log' file.
"""

import logging

from fdic_client import fetch_fdic_data
from s3_uploader import s3_uploader


def main():
    """Run the full FDIC ingestion pipeline.

    Configures logging with a timestamped format that writes to both a
    rotating file handler (``app.log``) and stdout, then calls
    ``fetch_fdic_data`` followed by ``s3_uploader`` in sequence.

    Raises:
        Exception: Any unhandled exception from either pipeline stage is
            logged as a critical error and re-raised so that the calling
            process receives a non-zero exit code.
    """

    # Configure logging once here so both imported modules inherit the same
    # handlers and format rather than each module's basicConfig taking effect
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info("Program started")

    try:
        all_data = fetch_fdic_data()
        s3_uploader(all_data)
    except Exception as e:
        logger.error(f"Critical error: {e}")
        raise


if __name__ == "__main__":
    main()
