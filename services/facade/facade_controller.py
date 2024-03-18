import facade_service
from domain.message import Message
from fastapi import FastAPI

app = FastAPI()


@app.post("/{msg}")
def post_message(msg: str):
    msg_obj = Message(text=msg)
    logs = facade_service.log_message(msg_obj)
    facade_service.add_message(msg_obj)
    return logs


@app.get("/")
def get_messages():
    return facade_service.get_messages()
