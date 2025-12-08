import logging
from config import settings

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.LOG_PATH),
            logging.StreamHandler()
        ]
    )
