import logging
from typing import Dict
from fastapi import FastAPI

app = FastAPI()

logger = logging.getLogger("uvicorn")
msg_map: Dict[str, str] = dict()


@app.get("/")
def post_message():
    return "Not Implemented Yet!"
