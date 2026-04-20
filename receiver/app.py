import connexion
from connexion import NoContent
from datetime import datetime, timezone
import time
import yaml
import logging
import logging.config
from kafka import KafkaProducer
from kafka.errors import KafkaError, NoBrokersAvailable
from threading import Lock
import json

# --- Helpers / Config ---

with open("/config/receiver_config.yml", "r") as file:
    app_config = yaml.safe_load(file.read())

with open("/config/receiver_log_config.yml", "r") as file1:
    LOG_CONFIG = yaml.safe_load(file1.read())
logging.config.dictConfig(LOG_CONFIG)

logger = logging.getLogger("basicLogger")

# Kafka config
KAFKA_HOST = app_config["kafka"]["hostname"]
KAFKA_PORT = app_config["kafka"]["port"]
KAFKA_TOPIC = app_config["kafka"]["topic"]

# Date helper function
def utc_now_z():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# --- Kafka Producer Wrapper ---

class KafkaProducerWrapper:
    def __init__(self, host, port, topic):
        self.bootstrap = f"{host}:{port}"
        self.topic = topic
        self.producer = None
        self.lock = Lock()

    def _connect(self):
        logger.info(f"Connecting Kafka producer to {self.bootstrap}")
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            linger_ms=5,
            acks=1
        )
        logger.info("Kafka producer connected")

    def get_producer(self):
        with self.lock:
            if self.producer is None:
                self._connect()
            return self.producer

    def reset(self):
        with self.lock:
            if self.producer is not None:
                try:
                    self.producer.close()
                except Exception:
                    pass
            self.producer = None

    def send_batch(self, events, retries=5, delay_seconds=1):
        """
        Send a batch of events to Kafka.
        Limited retries are used because this runs in an HTTP request path.
        """
        last_error = None

        for attempt in range(1, retries + 1):
            try:
                producer = self.get_producer()

                for event in events:
                    producer.send(self.topic, value=event)

                producer.flush()
                logger.info(f"Successfully sent batch of {len(events)} event(s) to Kafka")
                return True

            except (KafkaError, NoBrokersAvailable, OSError) as e:
                last_error = e
                logger.warning(
                    f"Kafka send failed on attempt {attempt}/{retries}: {e}"
                )
                self.reset()

                if attempt < retries:
                    time.sleep(delay_seconds)

            except Exception as e:
                last_error = e
                logger.exception(
                    f"Unexpected Kafka error on attempt {attempt}/{retries}: {e}"
                )
                self.reset()

                if attempt < retries:
                    time.sleep(delay_seconds)

        logger.error(f"Exhausted Kafka send retries. Last error: {last_error}")
        return False


kafka_wrapper = KafkaProducerWrapper(KAFKA_HOST, KAFKA_PORT, KAFKA_TOPIC)

# --- API Functions ---

def report_match_summaries(body):
    trace_id = time.time_ns()
    logger.info(f"Received event match_summaries with a trace id of {trace_id}")

    sender_id = body["sender_id"]
    sent_timestamp = body["sent_timestamp"]
    batch_id = body["batch_id"]

    items = body.get("items", []) or []
    events = []

    for item in items:
        flattened = {
            "type": "match_summaries",
            "datetime": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "payload": {
                "sender_id": sender_id,
                "sent_timestamp": sent_timestamp,
                "batch_id": batch_id,
                "trace_id": trace_id,
                **item
            }
        }
        events.append(flattened)

    ok = kafka_wrapper.send_batch(events)

    if not ok:
        return {"message": "Kafka unavailable. Please retry shortly."}, 503

    return NoContent, 201

def report_betting_odds(body):
    trace_id = time.time_ns()
    logger.info(f"Received event betting_odds with a trace id of {trace_id}")

    sender_id = body["sender_id"]
    sent_timestamp = body["sent_timestamp"]
    batch_id = body["batch_id"]

    items = body.get("items", []) or []
    events = []

    for item in items:
        flattened = {
            "type": "betting_odds",
            "datetime": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "payload": {
                "sender_id": sender_id,
                "sent_timestamp": sent_timestamp,
                "batch_id": batch_id,
                "trace_id": trace_id,
                **item
            }
        }
        events.append(flattened)

    ok = kafka_wrapper.send_batch(events)

    if not ok:
        return {"message": "Kafka unavailable. Please retry shortly."}, 503

    return NoContent, 201

def get_health():
    # Return health status for the Receiver service
    return {"message": "healthy"}, 200

def get_stats():
    # Return stats for the Receiver service
    return utc_now_z, 200

# --- App Setup ---

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml",
            base_path="/receiver",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")
