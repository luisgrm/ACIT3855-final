import connexion
import httpx
from connexion import NoContent
from datetime import datetime, timezone
import datetime
import yaml
import logging
import logging.config
import os
from threading import Lock
import json

# --- Helpers / Config ---

with open("/config/stats_config.yml", "r") as file:
    app_config = yaml.safe_load(file.read())

with open("/config/stats_log_config.yml", "r") as file1:
    LOG_CONFIG = yaml.safe_load(file1.read())
logging.config.dictConfig(LOG_CONFIG)

logger = logging.getLogger("basicLogger")

RECEIVER_URL = app_config["service_urls"]["receiver"]
STORAGE_URL = app_config["service_urls"]["storage"]
PROCESSING_URL = app_config["service_urls"]["processing"]
ANALYZER_URL = app_config["service_urls"]["analyzer"]
TIMEOUT = app_config["scheduler"]["timeout"]

STATS_PATH = os.path.join("/data", app_config["datastore"]["filename"])

def read_stats_file():
    if not os.path.exists(STATS_PATH):
        return None

    with open(STATS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def write_stats_file(stats):
    os.makedirs(os.path.dirname(STATS_PATH), exist_ok=True)

    with open(STATS_PATH, "w", encoding="utf-8") as file:
        json.dump(stats, file, indent=2)

def update_stats():
    num_available = 0

    receiver_status = "Unavailable"
    try:
        response = httpx.get(RECEIVER_URL, timeout=TIMEOUT)
        if response.status_code == 200:
            receiver_json = response.json()
            receiver_status = f"Receiver is healthy at ${datetime.now()}"
            logger.info("Receiver is healthy")
            num_available += 1
        else:
            logger.info("Receiver returning non-200 response")
    except (TimeoutError):
        logger.info("Receiver is not available")


    storage_status = "Unavailable"
    try:
        response = httpx.get(STORAGE_URL, timeout=TIMEOUT)
        if response.status_code == 200:
            storage_json = response.json()
            storage_status = f"Storage has "
            logger.info("Storage is healthy")
            num_available += 1
        else:
            logger.info("Storage returning non-200 response")
    except (TimeoutError):
        logger.info("Storage is not available")

    
    processing_status = "Unavailable"
    try:
        response = httpx.get(PROCESSING_URL, timeout=TIMEOUT)
        if response.status_code == 200:
            processing_json = response.json()
            processing_status = f"Processing has"
            logger.info("Processing is healthy")
            num_available += 1
        else:
            logger.info("Processing returning non-200 response")
    except (TimeoutError):
        logger.info("Processing is not available")

    analyzer_status = "Unavailable"
    try:
        response = httpx.get(ANALYZER_URL, timeout=TIMEOUT)
        if response.status_code == 200:
            analyzer_json = response.json()
            analyzer_status = f"Analyzer has"
            logger.info("Analyzer is healthy")
            num_available += 1
        else:
            logger.info("Analyzer returning non-200 response")
    except (TimeoutError):
        logger.info("Analyzer is not available")


    stats = {
        "receiver": receiver_status,
        "storage": storage_status,
        "processing": processing_status,
        "analyzer": analyzer_status,
    }

    return stats, 200

