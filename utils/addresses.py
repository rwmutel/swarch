from enum import StrEnum


class Address(StrEnum):
    FACADE = "http://facade:8000"
    LOGGER = "http://logger:8001"
    MESSAGES = "http://messages:8002"
