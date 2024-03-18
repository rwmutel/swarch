import logging
from contextlib import asynccontextmanager
import asyncio

import messages_service
from fastapi import FastAPI


logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI):
    messages_service.setup_client()
    asyncio.create_task(messages_service.listen())
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def get_message():
    return messages_service.get_messages()
