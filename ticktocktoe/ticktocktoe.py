import random
from uuid import uuid4

from ticktocktoe.types import GameState


class TickTockToe:
    def __init__(self, initial_size=3):
        self.id = uuid4().hex
        self.size = initial_size
        self.board = [['' for _ in range(self.size)] for _ in range(self.size)]
        self.choice_space = ['X', 'O']
        self.turn = 'X'
        self.state = GameState.INITIALIZED
        self.players = {}
        self.winner = None

    def to_json(self):
        return {
            'size': self.size,
            'board': self.board,
            'turn': self.turn,
            'players': self.players,
            'state': self.state.value,
            'winner': self.winner,
        }

    def play(self, player_id, i, j):
        if self.state != GameState.PLAYING:
            raise RuntimeError('Game not started')

        if player_id not in self.players:
            raise RuntimeError('Player not in game')
    
        if self.players[player_id] != self.turn:
            raise RuntimeError('It is not your turn')

        if self.board[i][j] == '':
            self.board[i][j] = self.turn
            self.turn = self.turn == 'X' and 'O' or 'X'
            self.winner = self.check_winner()
            if self.winner is not None:
                self.gameover()
        else:
            raise RuntimeError('Already taken')

    def is_join_possible(self):
        return len(self.players) < 2 and self.state == GameState.INITIALIZED

    def join(self, player):
        if self.state != GameState.INITIALIZED:
            print('Game already started')
            return
        
        if len(self.players) == 0:
            turn = random.choice(self.choice_space)
            self.choice_space.remove(turn)
            self.players[player] = turn
        elif len(self.players) == 1:
            turn = random.choice(self.choice_space)
            self.choice_space.remove(turn)
            self.players[player] = turn
            self.state = GameState.PLAYING
        else:
            print('Game already full')

    def check_winner(self):
        # Check rows and columns for a win
        for i in range(self.size):
            # Check row
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != "":
                return self.board[i][0]  # Return the winner ('X' or 'O')
            
            # Check column
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != "":
                return self.board[0][i]  # Return the winner ('X' or 'O')

        # Check diagonals for a win
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != "":
            return self.board[0][0]  # Return the winner ('X' or 'O')
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != "":
            return self.board[0][2]  # Return the winner ('X' or 'O')

        # Check for a draw (if all cells are filled and no winner)
        if all(cell != "" for row in self.board for cell in row):
            return "Draw"

        # No winner or draw, game continues
        return None


    def is_player_in_game(self, player_id: str):
        return player_id in self.players and self.state != GameState.FINISHED

    def gameover(self):
        self.state = GameState.FINISHED
