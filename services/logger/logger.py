import logging
import os
from contextlib import asynccontextmanager

import hazelcast
from hazelcast.proxy.map import Map
from domain.message import Message
from fastapi import FastAPI

logger = logging.getLogger("uvicorn")

hz_client: hazelcast.HazelcastClient = None
msg_map: Map = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.log(logging.INFO, "Starting Logging Server")
    logger.log(logging.INFO,
               f"Connecting to Hazelcast @ {os.environ['HZ_NODE_ADDRESS']}...")
    hz_client = hazelcast.HazelcastClient(cluster_name="lab-3",
                                          cluster_members=[
                                              os.environ["HZ_NODE_ADDRESS"]
                                          ])
    logger.log(logging.INFO, "Connected to Hazelcast")
    global msg_map
    msg_map = hz_client.get_map("messages").blocking()
    yield
    logger.log(logging.INFO,
               f"Stopping Logging Server Connected to Hazelcast Node at \
                {os.environ['HZ_NODE_ADDRESS']}")
    hz_client.shutdown()

app = FastAPI(lifespan=lifespan)


@app.post("/")
def post_message(msg: Message):
    msg_map.lock(msg.uid)
    if msg_map.contains_key(msg.uid):
        logger.warning(f"Message with id {msg.uid} is already in the map")
    msg_map.put(msg.uid, msg.text)
    msg_map.unlock(msg.uid)
    logger.info(
        f"Added {msg.text=} to map. Current messages: {msg_map.values()}")


@app.get("/")
def get_messages():
    return {"messages": list(msg_map.values())}
