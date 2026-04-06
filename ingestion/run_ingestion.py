import logging

from fdic_client import fetch_fdic_data
from s3_uploader import s3_uploader


def main():

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
