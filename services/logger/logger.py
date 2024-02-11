import logging

from fastapi import FastAPI

from utils.models.message import Message

app = FastAPI()

logger = logging.getLogger("uvicorn")
msg_map = dict()


@app.post("/")
def post_message(msg: Message):
    if msg.uid in msg_map:
        logger.warning(f"Message with id {msg.uid} is already in the map")
    msg_map[msg.uid] = msg.text
    logger.info(f"Current messages: {msg_map.values()}")


@app.get("/")
def get_messages():
    return {"messages": list(msg_map.values())}
