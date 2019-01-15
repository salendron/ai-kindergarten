import random
from model import get_model
import numpy as np

model = get_model()

class Player(object):

    def __init__(self,name):
        self.name = name


class HumanPlayer(Player):

    def get_move(self,game):
        while True:
            move = raw_input("{}: ".format(self.name))
            if game._is_valid_move(move):
                return move


class RandomPlayer(Player):

    def get_move(self,game):
        return random.choice(game.get_valid_moves())


class AIPlayer(Player):

    def get_move(self,game):
        predictions = model.predict(np.array([game.states[-1], ]))
        move = np.argmax(predictions[0])

        valid_moves = game.get_valid_moves()
        if move in valid_moves:
            # print("MOVE: {}".format(move))
            return move

        print("Invalid!")
        return random.choice(game.get_valid_moves())


class PartlyAIPlayer(Player):

    def get_move(self,game):
        if random.choice([True,False]):
            predictions = model.predict(np.array([game.states[-1], ]))
            move = np.argmax(predictions[0])

            valid_moves = game.get_valid_moves()
            if move in valid_moves:
                # print("MOVE: {}".format(move))
                return move

            #print("Invalid!")
            return random.choice(game.get_valid_moves())
        else:
            return random.choice(game.get_valid_moves())
