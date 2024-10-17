import json
from typing import Any

from m_types import ClientMessage, TTTEvent


def event_to_message(message: ClientMessage) -> str:
    return json.dumps({"type": message.event_type.value, "data": message.data})


def parse_event(event_message: str) -> ClientMessage:
    event = json.loads(event_message)
    return ClientMessage(
        event_type=TTTEvent(event["type"]), data=event["data"],
    )
