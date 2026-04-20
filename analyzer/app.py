import json
import logging
import logging.config
import yaml
import connexion
from kafka import KafkaConsumer
from connexion.middleware import MiddlewarePosition
from starlette.middleware.cors import CORSMiddleware
import os

# --- Config + Logging ---

with open("/config/analyzer_config.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

with open("/config/analyzer_log_config.yml", "r") as f:
    log_config = yaml.safe_load(f.read())
logging.config.dictConfig(log_config)

logger = logging.getLogger("basicLogger")

KAFKA_HOST = app_config["kafka"]["hostname"]
KAFKA_PORT = app_config["kafka"]["port"]
KAFKA_TOPIC = app_config["kafka"]["topic"]


# --- Kafka helpers ---

def make_history_consumer():
    # Creates a consumer that reads from the beginning of the topic history. 
    # We do NOT commit offsets because this service only INSPECTS history.
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}",
        auto_offset_reset="earliest",       # Reads from start of topic
        enable_auto_commit=False,           # Don't commit offsets (inspection-only)
        consumer_timeout_ms=1000,           # Stop after 1s with no more messages
    )
    return consumer


def find_nth_event_payload(event_type, index):
    # Kafka topic contains a MIX of event types.
    # index means: the Nth occurrence of that specific event_type while scanning from earliest.
    consumer = make_history_consumer()
    try:
        seen = 0

        for message in consumer:
            # message.value is bytes -> decode -> json.loads
            message_str = message.value.decode("utf-8")
            event = json.loads(message_str)

            if event.get("type") == event_type:
                if seen == index:
                    # Return only the payload according to my OpenAPI payload model
                    return event.get("payload")
                seen += 1

        return None
    finally:
        consumer.close()


def count_event_types():
    consumer = make_history_consumer()
    try:
        counts = {"match_summaries": 0, "betting_odds": 0}

        for message in consumer:
            message_str = message.value.decode("utf-8")
            event = json.loads(message_str)

            et = event.get("type")
            if et in counts:
                counts[et] += 1

        return counts
    finally:
        consumer.close()


# --- API endpoints ---

def get_match_summary_event(index):
    logger.info("GET /match-summaries?index=%s", index)

    # Manual validation - Connexion shouldnt pass strings
    try:
        idx = int(index)
        if idx < 0:
            raise ValueError()
    except Exception:
        return {"message": "index must be an integer >= 0"}, 400

    payload = find_nth_event_payload("match_summaries", idx)
    if payload is None:
        return {"message": f"No match_summaries event at index {idx}"}, 404

    return payload, 200


def get_betting_odds_event(index):
    logger.info("GET /betting-odds?index=%s", index)

    try:
        idx = int(index)
        if idx < 0:
            raise ValueError()
    except Exception:
        return {"message": "index must be an integer >= 0"}, 400

    payload = find_nth_event_payload("betting_odds", idx)
    if payload is None:
        return {"message": f"No betting_odds event at index {idx}"}, 404

    return payload, 200


def get_stats():
    logger.info("GET /stats")
    # API schema requires these keys:
    counts = count_event_types()
    return {
        "num_match_summaries": counts["match_summaries"],
        "num_betting_odds": counts["betting_odds"],
    }, 200

def get_health():
    # Return health status for the Analyzer service
    return {"message": "healthy"}, 200


# --- App setup ---

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
            base_path="/analyzer", 
            strict_validation=True, 
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8110, host="0.0.0.0")