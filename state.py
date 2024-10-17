import asyncio
from typing import Dict, Set
from websockets import WebSocketClientProtocol
from multipledispatch import dispatch

from event import event_to_message
from m_types import ClientMessage

connected_clients: Dict[str, WebSocketClientProtocol] = dict()


class StateManager:
    @staticmethod
    def add_client(client: WebSocketClientProtocol):
        connected_clients[client.id.hex] = client
        print(f"Client added: {client.id.hex}")

    @staticmethod
    def remove_client(client: WebSocketClientProtocol):
        del connected_clients[client.id.hex]
        print(f"Client removed: {client.id.hex}")

    @staticmethod
    async def send_event(client_id: str, message: ClientMessage):
        client = connected_clients.get(client_id, None)
        if client is None:
            return

        message = event_to_message(message)
        await client.send(message)

    @staticmethod
    async def broadcast_event(message: ClientMessage):
        if len(connected_clients) == 0:
            return
        
        message = event_to_message(message)
        tasks = [
            asyncio.create_task(client.send(message)) for client in connected_clients
        ]
        await asyncio.gather(*tasks)

    @staticmethod
    async def send_events(client_ids: Set[str], message: ClientMessage):
        if len(client_ids) == 0:
            return

        message = event_to_message(message)

        tasks = []
        for client_id in client_ids:
            client = connected_clients.get(client_id, None)
            if client is None:
                continue
            
            tasks.append(asyncio.create_task(client.send(message)))

        await asyncio.gather(*tasks)
