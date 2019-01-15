import argparse, time
from game import Game
from player import HumanPlayer, RandomPlayer, AIPlayer
from recorder import record_games
from train_data_loader import generate_replayable_games
from trainer import train


def __get_player(t, i):
    if t == "h":
        return HumanPlayer("[{}] Human".format(i))
    elif t == "r":
        return RandomPlayer("[{}] Random Player".format(i))
    elif t == "m":
        return AIPlayer("[{}] AI Player".format(i))

    raise Exception("Invalid Player Type: {}!".format(t))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p1", help="Player 1 - h = Human, m = Trained Model, r = Player that plays random moves")
    parser.add_argument("-p2", help="Player 2 - h = Human, m = Trained Model, r = Player that plays random moves")
    parser.add_argument("-r", help="Rounds to play - Number")
    args = parser.parse_args()

    p1 = __get_player(args.p1, 1)
    p2 = __get_player(args.p2, 2)
    r = int(args.r)

    games = []
    for i in range(r):
        if i % 2 == 0:
            p1 = __get_player(args.p1, 1)
            p2 = __get_player(args.p2, 2)
        else:
            p2 = __get_player(args.p1, 1)
            p1 = __get_player(args.p2, 2)

        g = Game(p1, p2, show_game=True)
        g.run()
        games.append(g)

        winner = g.get_winner()
        if winner == -1:
            print("Game ended in a tie.")
        else:
            print("Player {} won!".format(g.players[winner].name))

    file_name = record_games(games)

    print("\nREPLAYS!\n")
    time.sleep(1)
    replays = generate_replayable_games(file_name)
    record_games(replays)

    train()


