from dataclasses import dataclass
from enum import Enum, StrEnum
from typing import Any


@dataclass
class Mode:
    SEND = "SEND"
    READ = "READ"
    CONNECTION = "CONNECTION"


class ResponseLevel(Enum):
    SUCCESS = 0
    WARNING = 1
    CRITICAL = 2
    FAILURE = 3


@dataclass
class Response:
    result: bool
    command: str
    mode: str
    message: Any
