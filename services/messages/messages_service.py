import logging
from typing import Dict
import uuid
import asyncio

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import time

from utils.addresses import Address

logger = logging.getLogger("uvicorn")
msg_map: Dict[str, str] = dict()
consumer: KafkaConsumer = None
POLL_INTERVAL_MS = 200


def setup_client():
    global consumer
    while consumer is None:
        try:
            consumer = KafkaConsumer(
                "messages",
                bootstrap_servers=Address["KAFKA"],
                key_deserializer=lambda x: uuid.UUID(bytes=x),
                value_deserializer=lambda x: x.decode("utf-8")
            )
        except NoBrokersAvailable: 
            logger.critical("No Kafka brokers available! Retrying in 3 seconds...")
            time.sleep(3)
    logger.info("Consumer connected to Kafka topic")


def get_messages() -> Dict[str, str]:
    logger.info("Returning message map")
    return msg_map


async def listen():
    logger.info("Listening for messages")
    while True:
        raw_values = consumer.poll().values()
        msgs = [msg for topic_msgs in raw_values
                for msg in topic_msgs]
        if not msgs:
            logger.info(
                f"No messages received in the last {POLL_INTERVAL_MS}ms.")
        else:
            logger.info(f"Received msgs: {msgs}")
            for msg in msgs:
                msg_map[str(msg.key)] = msg.value
            logger.info(msg_map)
        await asyncio.sleep(POLL_INTERVAL_MS / 1000)
