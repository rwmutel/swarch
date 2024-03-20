import asyncio
import logging
from typing import Dict

import hazelcast

from utils.addresses import Address

logger = logging.getLogger("uvicorn")
msg_map: Dict[str, str] = dict()
POLL_INTERVAL_MS = 200
mq = None


def setup_client():
    global mq
    hz_client = hazelcast.HazelcastClient(
        cluster_name="lab-3-q",
        cluster_members=[Address["HZ_MQ"]]
    )
    mq = hz_client.get_queue("messages")
    logger.info("Connected to Hazelcast and initialized Message Queue")


def get_messages() -> Dict[str, str]:
    logger.info("Returning message map")
    return msg_map


async def listen():
    loop = asyncio.get_event_loop()
    logger.info("Listening for messages")
    while True:
        msg = await loop.run_in_executor(None, mq.take().result)
        logger.info(f"Received msg: {msg}")
        msg_map[msg["uid"]] = msg["text"]
