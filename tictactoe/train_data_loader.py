import json, datetime, os
from game_data_helper import get_winner_by_game_state
import numpy as np
from player import RandomPlayer, PartlyAIPlayer
from game import Game
from copy import deepcopy
from recorder import record_games
import time

DT_FORMAT = "%Y-%m-%d_%H-%M-%S"
TRAIN_DATA_PATH = './train_data/'
LAST_TRAIN_DATA_FILE = TRAIN_DATA_PATH + 'last_train.dat'

def get_last_train_date():
    if os.path.exists(LAST_TRAIN_DATA_FILE):
        with open(LAST_TRAIN_DATA_FILE, 'r') as f:
            d = f.read()
            return datetime.datetime.strftime(
                datetime.datetime.strptime(d, DT_FORMAT),
                DT_FORMAT
            )

    return datetime.datetime.strftime(
        datetime.datetime.strptime("1970-01-01_00-00-00", DT_FORMAT),
        DT_FORMAT
    )


def set_last_train_date():
    if os.path.exists(LAST_TRAIN_DATA_FILE):
        os.remove(LAST_TRAIN_DATA_FILE)

    with open(LAST_TRAIN_DATA_FILE, 'w') as f:
        f.write(datetime.datetime.now().strftime(DT_FORMAT))


def get_new_train_files():
    last_train = get_last_train_date()
    files = [s for s in os.listdir(TRAIN_DATA_PATH) if s.endswith('.json')]

    new_files = [
        f for f in files if f > last_train
    ]

    return new_files


def generate_replayable_games(file_name):
    with open(TRAIN_DATA_PATH + file_name, 'r') as fh:
        games = json.load(fh)["games"]

    new_games = []

    for game in games:
        original_game = Game(None,None)
        original_game.restore(game)

        rewind_game = Game(None, None, show_game=True)
        rewind_game.restore(game,rewind=2)
        rewind_game.play_move(original_game.moves[-1])
        new_games.append(rewind_game)

    return new_games

    """
        tie = False
        if original_winner == -1 and original_game.current_player == 1: #ties for player 1
            rewind_game = Game(None, None)
            rewind_game.restore(game, rewind=4)
            tie = True
            original_winner = 0
            rewind_game.players = [RandomPlayer("Random"), RandomPlayer("Random")]
        elif original_winner == 0:
            rewind_game.players = [RandomPlayer("Random"), PartlyAIPlayer("Random")]
        elif original_winner == 1:
            rewind_game.players = [PartlyAIPlayer("Random"), RandomPlayer("Random")]
        else:
            continue

        for i in range(10):
            new_winner = original_winner
            max_runs = 100
            runs = 0

            this_game = None
            while original_winner == new_winner and runs < max_runs:
                this_game = deepcopy(rewind_game)
                if not tie: this_game.play_move(original_game.moves[-1])
                new_winner = this_game.run()

                runs += 1

            if (new_winner != original_winner and new_winner != -1) or \
                    (new_winner == -1 and original_winner == 0 and not tie):
                new_games.append(this_game)

    print("{} replayed games generated.".format(len(new_games)))
    time.sleep(1)
    record_games(new_games)
    """


def load_train_data():
    files = get_new_train_files()

    games = []
    for f in files:
        with open(TRAIN_DATA_PATH + f, 'r') as fh:
            games += json.load(fh)["games"]

    x_data = []
    y_data = []
    for game in games:
        g = Game(None, None, show_game=False)
        g.restore(game)
        moves = g.moves

        # split game into player 1 and two
        split_up_game = [None, None]
        split_up_game[0] = [
            [moves[i] for i in range(len(moves)) if i % 2 == 0],
            [game[i] for i in range(len(game)) if i % 2 == 0]
        ]

        split_up_game[1] = [
            [moves[i] for i in range(len(moves)) if i % 2 != 0],
            [game[i] for i in range(len(game)) if i % 2 != 0]
        ]

        winner = get_winner_by_game_state(games[0][-1])

        # a tie counts as a win for player 1
        if winner == -1:
            winner = 1

        for i in range(len(split_up_game[winner])):
            # add game state (feature)
            x_data += split_up_game[winner][1][:len(split_up_game[winner][0])]

            # add right move to win (label)
            y_data += split_up_game[winner][0]

    x_train = np.array(x_data[0:int(len(x_data) / 2)])
    y_train = np.array(y_data[0:int(len(y_data) / 2)])

    x_test = np.array(x_data[int(len(x_data) / 2):])
    y_test = np.array(y_data[int(len(y_data) / 2):])

    return x_train, y_train, x_test, y_test
