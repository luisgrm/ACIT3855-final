import json
import logging.config
import os
from datetime import datetime

import connexion
import httpx
import yaml
from apscheduler.schedulers.background import BackgroundScheduler
from connexion.middleware import MiddlewarePosition
from starlette.middleware.cors import CORSMiddleware


with open("/config/health_log_config.yml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger("basicLogger")

with open("/config/health_config.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

SERVICE_PORT = app_config["service"]["port"]
SCHEDULER_INTERVAL = app_config["scheduler"]["interval"]
REQUEST_TIMEOUT = app_config["scheduler"]["timeout"]
HEALTH_URLS = app_config["health_urls"]
DATASTORE_FILE = app_config["datastore"]["filename"]


def get_health_status():
    # Return the currently stored health status data
    logger.info("Received request for health status")

    if not os.path.exists(DATASTORE_FILE):
        return {
            "receiver": "Unknown",
            "storage": "Unknown",
            "processing": "Unknown",
            "analyzer": "Unknown",
            "last_update": "Not available"
        }, 200

    with open(DATASTORE_FILE, "r") as f:
        data = json.load(f)

    return data, 200


def check_single_service(service_name, url):
    # Check one service health endpoint and return Up or Down
    try:
        response = httpx.get(url, timeout=REQUEST_TIMEOUT)

        if response.status_code == 200:
            logger.info("Recorded status for %s: Up", service_name)
            return "Up"

        logger.warning(
            "Recorded status for %s: Down (non-200 response: %s)",
            service_name,
            response.status_code
        )
        return "Down"

    except Exception as e:
        logger.warning("Recorded status for %s: Down (%s)", service_name, str(e))
        return "Down"


def populate_health_status():
    # Poll all backend services and write their current health statuses
    logger.info("Starting scheduled health check")

    status_data = {
        "receiver": check_single_service("receiver", HEALTH_URLS["receiver"]),
        "storage": check_single_service("storage", HEALTH_URLS["storage"]),
        "processing": check_single_service("processing", HEALTH_URLS["processing"]),
        "analyzer": check_single_service("analyzer", HEALTH_URLS["analyzer"]),
        "last_update": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    }

    os.makedirs(os.path.dirname(DATASTORE_FILE), exist_ok=True)

    with open(DATASTORE_FILE, "w") as f:
        json.dump(status_data, f, indent=2)

    logger.info("Wrote health status snapshot to %s", DATASTORE_FILE)


def init_scheduler():
    # Initialize the scheduler for periodic health checks
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(
        populate_health_status,
        "interval",
        seconds=SCHEDULER_INTERVAL
    )
    sched.start()
    logger.info("Scheduler started. Interval=%s", SCHEDULER_INTERVAL)


app = connexion.FlaskApp(__name__, specification_dir="")

# app.add_middleware(
#     CORSMiddleware,
#     position=MiddlewarePosition.BEFORE_EXCEPTION,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

if "CORS_ALLOW_ALL" in os.environ and os.environ["CORS_ALLOW_ALL"] == "yes":
    app.add_middleware(
        CORSMiddleware,
        position=MiddlewarePosition.BEFORE_EXCEPTION,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_api("openapi.yml",
            base_path="/health",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    populate_health_status()
    init_scheduler()
    app.run(port=SERVICE_PORT, host="0.0.0.0")