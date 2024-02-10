import uuid
import requests
import logging

from fastapi import FastAPI

from utils.addresses import Address

app = FastAPI()

logger = logging.getLogger("uvicorn")


@app.post("/{msg}")
def post_message(msg):
    uid = str(uuid.uuid4())
    payload = {"uid": uid, "text": msg}
    res = requests.post(url=Address.LOGGER, json=payload)
    if res.status_code != 200:
        logger.critical("Error sending POST request to logging service!")
    else:
        logger.info(
            f"Sent POST request with message {msg}" +
            f"with uuid {uid} to logging service")


@app.get("/")
def get_messages():
    log_res = requests.get(url=Address.LOGGER)
    if log_res.status_code != 200:
        logger.critical("Error sending GET request to logging service!")

    msg_res = requests.get(url=Address.MESSAGES)
    if msg_res.status_code != 200:
        logger.critical("Error sending GET request to messages service!")

    messages_service_data = msg_res.text
    logging_service_data = log_res.json()["messages"]
    logger.info(
        f"GET request to logging service result: {logging_service_data}")
    logger.info(
        f"GET request to messages service result: {messages_service_data}")
    return str(logging_service_data) + "; " + str(messages_service_data)
