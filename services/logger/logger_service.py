import logging
import os
from typing import List

import hazelcast
from domain.message import Message

logger = logging.getLogger("uvicorn")


class HazelcastLogger:
    MAP_NAME = "messages"

    def __init__(self, cluster_name: str, cluster_members: List[str]):
        self.cluster_name = cluster_name
        self.cluster_members = cluster_members
        logger.log(logging.INFO,
                   "Connecting to Hazelcast @ "
                   f"{os.environ['HZ_NODE_ADDRESS']}...")
        self.client = hazelcast.HazelcastClient(
            cluster_name=cluster_name,
            cluster_members=cluster_members)
        self.msg_map = self.client.get_map(self.MAP_NAME).blocking()

    def add_message(self, msg: Message):
        self.msg_map.lock(msg.uid)
        if self.msg_map.contains_key(msg.uid):
            logger.warning(f"Message with id {msg.uid} is already in the map")
        self.msg_map.put(msg.uid, msg.text)
        self.msg_map.unlock(msg.uid)

    def get_messages(self) -> List[str]:
        return list(self.msg_map.values())

    def __del__(self):
        self.client.shutdown()
