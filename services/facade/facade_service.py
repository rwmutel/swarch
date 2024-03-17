import logging
import random
import uuid

import requests

from utils.addresses import Address

logger = logging.getLogger("uvicorn")


def add_message(msg: str):
    uid = str(uuid.uuid4())
    payload = {"uid": uid, "text": msg}
    logger_url: str = random.choice(Address["LOGGERS"])
    res = requests.post(url=logger_url, json=payload)
    if res.status_code != 200:
        logger.critical(
            f"Error sending POST request to logging service at {logger_url}!")
        return "Error sending POST request to logging service!"
    else:
        logger.info(
            f"Sent POST request with message {msg}" +
            f"with uuid {uid} to logging service at {logger_url}")
        return (f"Added message {msg} with uuid {uid} "
                f"to logging service at {logger_url}")


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
