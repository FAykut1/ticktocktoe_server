from typing import Dict
from m_types import ClientMessage, TTTEvent
from state import StateManager
from ticktocktoe.ticktocktoe import TickTockToe


class Gamemanager:
    def __init__(self):
        self.games: Dict[str, TickTockToe] = {}

    def create_game(self, size):
        game = TickTockToe(size)
        self.games[game.id] = game
        print(f"Game {game.id} created")
        return game.id

    async def leave_game(self, player_id: str):
        game_id = self.get_game_id_from_player(player_id)
        if game_id is None:
            return
        
        game = self.games[game_id]
        game.gameover()
        await self.send_update_board_event(game_id)

    def find_available_game(self):
        for game in self.games.values():
            if game.is_join_possible():
                return game.id

    async def join_game(self, game_id, player_id):
        game = self.games[game_id]
        game.join(player_id)
        print(f"Player {player_id} joined game {game_id}")
        await self.send_update_board_event(game_id)

    def get_game_id_from_player(self, player_id: str) -> str:
        for game in self.games.values():
            if game.is_player_in_game(player_id):
                return game.id

        return None

    def get_game_state(self, game_id):
        game = self.games[game_id]
        return game.to_json()

    def play(self, game_id, player_id, i, j):
        game = self.games[game_id]
        game.play(player_id, i, j)
        print(f"Player {player_id} played in game {game_id}")

    async def send_update_board_event(self, game_id):
        game = self.games[game_id]
        player_ids = list(game.players.keys())
        
        await StateManager.send_events(player_ids, ClientMessage(TTTEvent.UPDATE_BOARD, game.to_json()))


gamemanager = Gamemanager()
