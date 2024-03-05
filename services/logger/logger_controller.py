import logging
import os
from contextlib import asynccontextmanager
from domain.message import Message
from logger_service import HazelcastLogger
from fastapi import FastAPI

logger = logging.getLogger("uvicorn")
hz_logger: HazelcastLogger = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.log(logging.INFO, "Starting Logging Server using Hazelcast Logger")
    global hz_logger
    hz_logger = HazelcastLogger(cluster_name="lab-3",
                                cluster_members=[os.environ["HZ_NODE_ADDRESS"]])
    yield
    del hz_logger

app = FastAPI(lifespan=lifespan)


@app.post("/")
def post_message(msg: Message):
    hz_logger.add_message(msg)
    logger.info(
        f"Added {msg.text=} to map. "
        f"Current messages: {hz_logger.get_messages()}")


@app.get("/")
def get_messages():
    msg_list = hz_logger.get_messages()
    return {"messages": msg_list}
