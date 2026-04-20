import connexion
import logging
import logging.config
import yaml
from datetime import datetime, timezone
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from connexion.middleware import MiddlewarePosition
from starlette.middleware.cors import CORSMiddleware

# --- Logger Config ---

with open("/config/processing_log_config.yml", "r") as file:
    LOG_CONFIG = yaml.safe_load(file.read())
logging.config.dictConfig(LOG_CONFIG)

logger = logging.getLogger("basicLogger")

# --- App Config ---

with open("/config/processing_config.yml", "r") as file:
    app_config = yaml.safe_load(file.read())

# --- JSON Stats Helpers ---

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

def utc_now_z():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# --- Periodically Called Job ---

def populate_stats():
    logger.info("Periodic processing started")

    end_ts = utc_now_z()
    start_ts = "1970-01-01T00:00:00Z"

    match_url = app_config["eventstore"]["match_summaries"]["url"]
    bet_url = app_config["eventstore"]["betting_odds"]["url"]

    match_events = []
    betting_events = []
    match_resp = None
    bet_resp = None

    try:
        match_resp = requests.get(
            match_url,
            params={"start_timestamp": start_ts, "end_timestamp": end_ts},
            timeout=10
        )
        if match_resp.status_code == 200:
            match_events = match_resp.json()
        else:
            logger.error(
                "Match summaries fetch failed: status=%s body=%s",
                match_resp.status_code, match_resp.text
            )
    except requests.exceptions.RequestException as e:
        logger.error("Match summaries fetch failed: %s", str(e))

    try:
        bet_resp = requests.get(
            bet_url,
            params={"start_timestamp": start_ts, "end_timestamp": end_ts},
            timeout=10
        )
        if bet_resp.status_code == 200:
            betting_events = bet_resp.json()
        else:
            logger.error(
                "Betting odds fetch failed: status=%s body=%s",
                bet_resp.status_code, bet_resp.text
            )
    except requests.exceptions.RequestException as e:
        logger.error("Betting odds fetch failed: %s", str(e))

    logger.info("Received %d match summaries", len(match_events))
    logger.info("Received %d betting odds", len(betting_events))

    match_ok = (match_resp is not None and match_resp.status_code == 200)
    bet_ok = (bet_resp is not None and bet_resp.status_code == 200)

    if not (match_ok and bet_ok):
        logger.warning(
            "Not updating stats because a storage call failed. match_ok=%s bet_ok=%s",
            match_ok, bet_ok
        )
        return

    previous_stats = read_stats_file()
    if previous_stats is None:
        previous_stats = {
            "num_match_summaries": 0,
            "num_betting_odds": 0,
            "max_home_goals": 0,
            "max_odds": 0,
            "last_updated": "1970-01-01T00:00:00Z"
        }

    stats = {
        "num_match_summaries": len(match_events),
        "num_betting_odds": len(betting_events),
        "max_home_goals": 0,
        "max_odds": 0,
        "last_updated": previous_stats["last_updated"]
    }

    if match_events:
        stats["max_home_goals"] = max(int(event.get("home_goals", 0)) for event in match_events)

    if betting_events:
        stats["max_odds"] = max(float(event.get("odds", 0)) for event in betting_events)

    # Only update last_updated if something actually changed
    if (
        stats["num_match_summaries"] != previous_stats["num_match_summaries"] or
        stats["num_betting_odds"] != previous_stats["num_betting_odds"] or
        stats["max_home_goals"] != previous_stats["max_home_goals"] or
        stats["max_odds"] != previous_stats["max_odds"]
    ):
        stats["last_updated"] = end_ts

    write_stats_file(stats)

    logger.debug("Updated stats: %s", stats)
    logger.info("Periodic processing ended")

def init_scheduler():
    interval = app_config["scheduler"]["interval"]
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(
        populate_stats,
        "interval",
        seconds=interval,
        max_instances=1,
        coalesce=True
    )
    sched.start()
    logger.info("Scheduler started. Interval=%s", interval)

# --- GET Endpoints ---

def get_stats():
    logger.info("GET /stats request received")

    stats = read_stats_file()
    if stats is None:
        logger.error("Statistics file does not exist")
        return {"message": "Statistics do not exist"}, 404

    logger.debug("Statistics contents: %s", stats)
    logger.info("GET /stats request completed")
    return stats, 200

def get_health():
    return {"message": "healthy"}, 200

# --- App Setup ---

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
            base_path="/processing",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, host="0.0.0.0")