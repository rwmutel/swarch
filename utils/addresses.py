from typing import Dict, List

Address: Dict[str, str | List[str]] = {
    "FACADE": "http://facade:8000",
    "LOGGERS": ["http://logger-1:8001",
                "http://logger-2:8001",
                "http://logger-3:8001"
                ],
    "MESSAGES": "http://messages:8002"
}
