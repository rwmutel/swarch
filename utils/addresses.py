from enum import Enum
from typing import List


class Address(Enum):
    FACADE = "http://facade:8000"
    LOGGERS: List[str] = ["http://logger-1:8001",
                          "http://logger-2:8001",
                          "http://logger-3:8001"]
    MESSAGES = "http://messages:8002"
