import logging
import random
import time

import requests
from domain.message import Message
import hazelcast

from utils.addresses import Address

logger = logging.getLogger("uvicorn")
mq = None


def setup_mq():
    global mq
    hz_client = hazelcast.HazelcastClient(
        cluster_name="lab-3-q",
        cluster_members=[Address["HZ_MQ"]]
    )
    mq = hz_client.get_queue("messages")
    logger.info("Connected to Hazelcast and initialized Message Queue")


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
            f"Sent POST request with message {msg.text} " +
            f"with uuid {str(msg.uid)} to logging service at {logger_url}")
        return (f"Added message {msg.text} with uuid {str(msg.uid)} "
                f"to logging service at {logger_url}")


def add_message(msg: Message):
    mq.put(msg.model_dump(mode="json")).result()
    logger.info(f"Sent message {msg.text} with uuid "
                f"{str(msg.uid)} to Hazelcast Message Queue")


def get_messages():
    log_res = requests.get(
        url=(logger_url := random.choice(Address["LOGGERS"])))
    if log_res.status_code != 200:
        logger.critical(
            f"Error sending GET request to logging service at {logger_url}!")

    msg_res = requests.get(url=(msg_url := random.choice(Address["MESSAGES"])))
    if msg_res.status_code != 200:
        logger.critical(
            f"Error sending GET request to messages service at {msg_url}!")

    messages_service_data = msg_res.text
    logging_service_data = log_res.json()["messages"]
    logger.info(
        f"GET request to logging service (at {logger_url}) "
        f"result: {logging_service_data}")
    logger.info(
        f"GET request to messages service (at {msg_url}) "
        f"result: {messages_service_data}")
    return str(logging_service_data) + "; " + str(messages_service_data)
