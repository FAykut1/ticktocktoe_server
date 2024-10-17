from enum import IntEnum, StrEnum


class GameState(StrEnum):
    INITIALIZED = "INITIALIZED"
    PLAYING = "PLAYING"
    FINISHED = "FINISHED"
