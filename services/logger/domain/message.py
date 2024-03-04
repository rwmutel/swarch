import uuid

from pydantic import BaseModel


class Message(BaseModel):
    text: str
    uid: uuid.UUID
