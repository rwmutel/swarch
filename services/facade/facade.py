import logging
import random
import uuid

import requests
from fastapi import FastAPI

from utils.addresses import Address

app = FastAPI()

logger = logging.getLogger("uvicorn")


@app.post("/{msg}")
def post_message(msg: str):
    uid = str(uuid.uuid4())
    payload = {"uid": uid, "text": msg}
    logger_url: str = random.choice(Address.LOGGERS)
    res = requests.post(url=logger_url, json=payload)
    if res.status_code != 200:
        logger.critical(
            f"Error sending POST request to logging service at {logger_url}!")
    else:
        logger.info(
            f"Sent POST request with message {msg}" +
            f"with uuid {uid} to logging service at {logger_url}")


@app.get("/")
def get_messages():
    logger_url = random.choice(Address.LOGGERS)
    log_res = requests.get(url=logger_url)
    if log_res.status_code != 200:
        logger.critical(
            f"Error sending GET request to logging service at {logger_url}!")

    msg_res = requests.get(url=Address.MESSAGES)
    if msg_res.status_code != 200:
        logger.critical("Error sending GET request to messages service!")

    messages_service_data = msg_res.text
    logging_service_data = log_res.json()["messages"]
    logger.info(
        f"GET request to logging service (at {logger_url}) \
            result: {logging_service_data}")
    logger.info(
        f"GET request to messages service result: {messages_service_data}")
    return str(logging_service_data) + "; " + str(messages_service_data)
