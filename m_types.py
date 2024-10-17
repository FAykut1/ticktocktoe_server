from enum import IntEnum
from typing import Any, NamedTuple


class TTTEvent(IntEnum):
    JOIN_GAME = 1
    PLAY = 2
    UPDATE_BOARD = 3
    ERROR = 4


class ClientMessage(NamedTuple):
    event_type: TTTEvent
    data: Any
