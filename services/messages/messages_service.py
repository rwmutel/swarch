import logging
from typing import Dict
import asyncio

from confluent_kafka import Consumer, KafkaException
import time
import os

from utils.addresses import Address

logger = logging.getLogger("uvicorn")
msg_map: Dict[str, str] = dict()
consumer: Consumer = None
GROUP_ID = os.environ.get("KAFKA_GROUP_ID")
POLL_INTERVAL_MS = 200


def setup_client():
    global consumer
    while consumer is None:
        try:
            consumer = Consumer(
                {
                    "bootstrap.servers": Address["KAFKA"],
                    "group.id": GROUP_ID,
                    "enable.auto.offset.store": True,
                    "auto.offset.reset": "earliest"
                }
            )
            consumer.subscribe(["messages"])
        except KafkaException as e:
            logger.critical(
                "No Kafka brokers available! Retrying in 3 seconds...")
            logger.critical(e.args[0])
            time.sleep(3)
    logger.info("Consumer connected to Kafka topic")


def get_messages() -> Dict[str, str]:
    logger.info("Returning message map")
    return msg_map


async def listen():
    loop = asyncio.get_running_loop()
    logger.info("Listening for messages")
    while True:
        raw_message = await loop.run_in_executor(
            None,
            lambda: consumer.poll(timeout=0.05)
        )
        # raw_messages = consumer.poll(timeout=0.1)
        if not raw_message:
            logger.info(
                f"No messages received in the last {POLL_INTERVAL_MS}ms.")
        else:
            logger.info(
                f"Received msgs: {raw_message.key()}: {raw_message.value()}")
            msg_map[str(raw_message.key())] = \
                raw_message.value().decode("utf-8")
        await asyncio.sleep(POLL_INTERVAL_MS / 1000)
