import asyncio
from typing import Dict
from websockets.server import serve
from websockets.exceptions import ConnectionClosed
from websockets import WebSocketServerProtocol
import logging

from event import parse_event
from m_types import ClientMessage, TTTEvent
from state import StateManager
from ticktocktoe.gamemanager import gamemanager
from ticktocktoe.ticktocktoe import TickTockToe


logger = logging.getLogger("main")


async def handle_connection(websocket: WebSocketServerProtocol):
    StateManager.add_client(websocket)
    client_id = websocket.id.hex
    
    try:
        async for message in websocket:
            try:
                _type, data = parse_event(message)

                print(f"Received message from {websocket.remote_address}: {message}")

                if _type == TTTEvent.JOIN_GAME:
                    if gamemanager.get_game_id_from_player(client_id) is not None:
                        raise RuntimeError("Player already in game")
                    
                    game_id = gamemanager.find_available_game()
                    if game_id is None:
                        game_id = gamemanager.create_game(3)
                    
                    await gamemanager.join_game(game_id, client_id)
                elif _type == TTTEvent.PLAY:
                    i, j = data["pos"]
                    game_id = gamemanager.get_game_id_from_player(client_id)
                    if game_id is None:
                        raise RuntimeError("Player not in game")

                    gamemanager.play(game_id, client_id, i, j)
                    await gamemanager.send_update_board_event(game_id)

            except Exception as e:
                await StateManager.send_event(client_id, ClientMessage(TTTEvent.ERROR, {"message": str(e)}))
                logger.exception(f"Error processing message from {client_id}")
    except ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")
    finally:
        try:
            StateManager.remove_client(websocket)
            await gamemanager.leave_game(client_id)
        except Exception as e:
            logger.exception(f"Error removing client {client_id}")


async def main():
    async with serve(handle_connection, "localhost", 8765):
        await asyncio.get_running_loop().create_future()  # run forever


asyncio.run(main())
