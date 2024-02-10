from enum import StrEnum


class Address(StrEnum):
    FACADE = "http://127.0.0.1:8000"
    LOGGER = "http://127.0.0.1:8001"
    MESSAGES = "http://127.0.0.1:8002"
