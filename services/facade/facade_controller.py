import facade_service

from fastapi import FastAPI

app = FastAPI()


@app.post("/{msg}")
def post_message(msg: str):
    return facade_service.add_message(msg)


@app.get("/")
def get_messages():
    return facade_service.get_messages()
