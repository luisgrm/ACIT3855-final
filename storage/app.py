import connexion
from connexion import NoContent
import functools
from db import make_session
from models import MatchSummary, BettingOdds
import logging
import logging.config
import yaml
from datetime import datetime, timezone
from sqlalchemy import select

import json
import time
from threading import Thread
from kafka import KafkaConsumer
from kafka.errors import KafkaError, NoBrokersAvailable

# --- Logging Setup ---

with open("/config/storage_log_config.yml", "r") as file:
    LOG_CONFIG = yaml.safe_load(file.read())
logging.config.dictConfig(LOG_CONFIG)

logger = logging.getLogger("basicLogger")

# --- App Config ---
with open("/config/storage_config.yml", "r") as file:
    app_config = yaml.safe_load(file.read())

KAFKA_HOST = app_config["kafka"]["hostname"]
KAFKA_PORT = app_config["kafka"]["port"]
KAFKA_TOPIC = app_config["kafka"]["topic"]
KAFKA_GROUP = app_config["kafka"].get("consumer_group", "storage_group")

# --- Helpers ---

def parse_datetime(dt_str):
    if dt_str.endswith("Z"):
        dt_str = dt_str[:-1] + "+00:00"
    dt = datetime.fromisoformat(dt_str)
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt

# --- Storage DB Session Decorator ---

# Decorator
def use_db_session(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        session = make_session()
        try:
            return func(session, *args, **kwargs)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    return wrapper

# --- POST Endpoints ---

# Stores 1 MatchSummaryEvent into the database
@use_db_session
def store_match_summary(session, body):
    trace_id = body["trace_id"]

    event = MatchSummary(
        sender_id=body["sender_id"],
        sent_timestamp=body["sent_timestamp"],
        batch_id=body["batch_id"],
        trace_id=body["trace_id"],
        match_id=body["match_id"],
        league=body["league"],
        season=body["season"],
        match_date=body["match_date"],
        home_team_id=body["home_team_id"],
        home_team_name=body["home_team_name"],
        away_team_id=body["away_team_id"],
        away_team_name=body["away_team_name"],
        home_goals=body["home_goals"],
        away_goals=body["away_goals"],
        result=body["result"]
    )

    session.add(event)
    session.commit()
    logger.debug(f"Stored event match_summaries with a trace id of {trace_id}")
    return NoContent, 201

# Stores 1 BettingOddsEvent into the database
@use_db_session
def store_betting_odds(session, body):
    trace_id = body["trace_id"]

    event = BettingOdds(
        sender_id=body["sender_id"],
        sent_timestamp=body["sent_timestamp"],
        batch_id=body["batch_id"],
        trace_id=body["trace_id"],
        match_id=body["match_id"],
        bookmaker=body["bookmaker"],
        market=body["market"],
        outcome=body["outcome"],
        odds=body["odds"],
        odds_type=body["odds_type"],
        collected_at=body["collected_at"]
    )

    session.add(event)
    session.commit()
    logger.debug(f"Stored event betting_odds with a trace id of {trace_id}")
    return NoContent, 201

# --- Kafka Consumer Helpers ---

def make_consumer():
    bootstrap = f"{KAFKA_HOST}:{KAFKA_PORT}"
    logger.info(
        f"Creating Kafka consumer (bootstrap={bootstrap}, topic={KAFKA_TOPIC}, group={KAFKA_GROUP})"
    )

    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=bootstrap,
        group_id=KAFKA_GROUP,
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )
    return consumer


def process_single_message(consumer, msg):
    logger.info(f"Kafka message received: {msg}")

    event_type = msg.get("type")
    payload = msg.get("payload")

    if not event_type or payload is None:
        logger.warning("Skipping message missing type/payload")
        consumer.commit()
        return

    if event_type == "match_summaries":
        store_match_summary(payload)
    elif event_type == "betting_odds":
        store_betting_odds(payload)
    else:
        logger.warning(f"Unknown event type: {event_type}. Skipping.")

    # Commit offset only after successful processing
    consumer.commit()


# --- Kafka Consumer Thread with Retry Logic ---

def process_messages():
    """
    Infinite retry loop:
    - tries to connect to Kafka
    - consumes messages
    - if Kafka fails, logs the issue, waits, reconnects, and continues
    """
    while True:
        consumer = None

        try:
            consumer = make_consumer()
            logger.info("Kafka consumer connected successfully")

            for message in consumer:
                try:
                    process_single_message(consumer, message.value)
                except Exception as e:
                    logger.exception(f"Error processing Kafka message: {e}")
                    # No commit here -> at-least-once retry behavior

        except (KafkaError, NoBrokersAvailable, OSError) as e:
            logger.warning(f"Kafka consumer issue. Will retry connection: {e}")
            time.sleep(2)

        except Exception as e:
            logger.exception(f"Unexpected storage Kafka loop error: {e}")
            time.sleep(2)

        finally:
            if consumer is not None:
                try:
                    consumer.close()
                except Exception:
                    pass


def setup_kafka_thread():
    thread = Thread(target=process_messages)
    thread.daemon = True
    thread.start()

# --- GET Endpoints ---
# Get MatchSummary events between timestamps
@use_db_session
def get_match_summaries(session, start_timestamp, end_timestamp):
    start = parse_datetime(start_timestamp)
    end = parse_datetime(end_timestamp)

    if start >= end:
        return {"message": "start_timestamp must be earlier than end_timestamp"}, 400

    statement = (
        select(MatchSummary)
        .where(MatchSummary.date_created >= start)
        .where(MatchSummary.date_created < end)
        .order_by(MatchSummary.date_created)
    )

    rows = session.execute(statement).scalars().all()
    results = []
    for row in rows:
        results.append(row.to_dict())
    
    logger.debug("Found %d match summaries (start=%s end=%s)",
        len(results), start_timestamp, end_timestamp)
    
    return results, 200


# Get BettingOdds events between timestamps
@use_db_session
def get_betting_odds(session, start_timestamp, end_timestamp):
    start = parse_datetime(start_timestamp)
    end = parse_datetime(end_timestamp)

    if start >= end:
        return {"message": "start_timestamp must be earlier than end_timestamp"}, 400

    statement = (
        select(BettingOdds)
        .where(BettingOdds.date_created >= start)
        .where(BettingOdds.date_created < end)
        .order_by(BettingOdds.date_created)
    )

    rows = session.execute(statement).scalars().all()
    results = []
    for row in rows:
        results.append(row.to_dict())
    
    logger.debug("Found %d betting odds (start=%s end=%s)",
        len(results), start_timestamp, end_timestamp)
    
    return results, 200

def get_health():
    # Return health status for the Storage service
    return {"message": "healthy"}, 200

@use_db_session
def get_event_statsget_event_stats(session):
    statement1 = (
        select(BettingOdds)
    )

    rows = session.execute(statement1).scalars().all()
    num_match_summaries = 0
    for row in rows:
        num_match_summaries += 1

    statement2 = (
        select(BettingOdds)
    )

    rows = session.execute(statement2).scalars().all()
    num_betting_odds = 0
    for row in rows:
        num_betting_odds += 1
    
    return num_match_summaries, num_betting_odds, 200

# --- App Setup ---

app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yml",
            base_path="/storage",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    setup_kafka_thread()
    app.run(port=8090, host="0.0.0.0")
