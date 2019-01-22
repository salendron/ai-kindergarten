import jwt
from .jwt_secret import SECRET
from copy import deepcopy
import random


class Game(object):

    def __init__(self):
        self.players = self.choose_players()
        self.current_player = 0
        self.states = []
        self.moves = []

    def choose_players(self):
        players = ['h','m']
        random.shuffle(players)
        return players

    def start(self):
            #generate empty board
            self.states.append(
                [-1,-1,-1,-1,-1,-1,-1,-1,-1]
            )

    @classmethod
    def from_token(cls, token):
        game = Game()

        try:
            payload = jwt.decode(token,SECRET, algorithms=['HS256'])

            game.players = payload['players']
            game.current_player = payload['current-player']
            game.states = payload['states']
            game.moves = payload['moves']

            return game
        except Exception as ex:
            game.start()

        return game

    def to_token(self):
        payload = {
            'players': self.players,
            'current-player': self.current_player,
            'states': self.states,
            'moves': self.moves
        }

        return jwt.encode(payload, SECRET, algorithm='HS256').decode('unicode_escape')

    def _is_valid_move(self, move):
        try:
            move = int(move)
        except ValueError:
            return False

        if move < 0 or move > 8:
            return False

        if move not in self.get_valid_moves():
            return False

        return True

    def get_valid_moves(self):
        current_state = self.states[-1]

        valid_moves = []
        for i in range(9):
            if current_state[i] == -1:
                valid_moves.append(i)

        return valid_moves

    def play(self, move):
        if not self._is_valid_move(move):
            raise Exception("Invalid move!")

        move = int(move)

        new_state = deepcopy(self.states[-1])
        new_state[move] = self.current_player

        self.states.append(new_state)
        self.moves.append(move)

        self.current_player = 1 if self.current_player == 0 else 0

    def get_winner(self):
        current_state = self.states[-1]

        #check each player
        for p in range(2):

            # check each row
            for r in range(3):
                f1 = r * 3
                if current_state[f1] == p and current_state[f1 + 1] == p and current_state[f1 + 2] == p:
                    return p

            # check each column
            for c in range(3):
                if current_state[c] == p and current_state[c + 3] == p and current_state[c + 6] == p:
                    return p

            # check diagonal
            if current_state[0] == p and current_state[4] == p and current_state[8] == p:
                return p

            if current_state[2] == p and current_state[4] == p and current_state[6] == p:
                return p

        # check for a tie
        moves_played = 0
        for f in current_state:
            if f != -1:
                moves_played += 1

        if moves_played == 9:
            return 2

        return -1
