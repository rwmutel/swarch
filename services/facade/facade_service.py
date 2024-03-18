import logging
import random

import requests
from domain.message import Message
from kafka.producer import KafkaProducer

from utils.addresses import Address

logger = logging.getLogger("uvicorn")
mq_producer = KafkaProducer(bootstrap_servers=Address["KAFKA"],
                            value_serializer=str.encode)


def log_message(msg: Message):
    logger_url: str = random.choice(Address["LOGGERS"])
    res = requests.post(url=logger_url, json=msg.model_dump(mode="json"))
    if res.status_code != 200:
        logger.critical(
            f"Error sending POST request to logging service at {logger_url}! "
            f"Details: {res.json()}")
        return "Error sending POST request to logging service!"
    else:
        logger.info(
            f"Sent POST request with message {msg.text}" +
            f"with uuid {str(msg.uid)} to logging service at {logger_url}")
        return (f"Added message {msg.text} with uuid {str(msg.uid)} "
                f"to logging service at {logger_url}")


def add_message(msg: Message):
    mq_producer.send(topic="messages",
                     key=msg.uid.bytes,
                     value=msg.text).get()
    logger.info(f"Sent message {msg.text} with uuid "
                f"{str(msg.uid)} to Kafka Message Queue")


def get_messages():
    logger_url = random.choice(Address["LOGGERS"])
    log_res = requests.get(url=logger_url)
    if log_res.status_code != 200:
        logger.critical(
            f"Error sending GET request to logging service at {logger_url}!")

    msg_res = requests.get(url=Address["MESSAGES"])
    if msg_res.status_code != 200:
        logger.critical("Error sending GET request to messages service!")

    messages_service_data = msg_res.text
    logging_service_data = log_res.json()["messages"]
    logger.info(
        f"GET request to logging service (at {logger_url})"
        f"result: {logging_service_data}")
    logger.info(
        f"GET request to messages service result: {messages_service_data}")
    return str(logging_service_data) + "; " + str(messages_service_data)
