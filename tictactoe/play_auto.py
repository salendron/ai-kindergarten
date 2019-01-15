import argparse
from game import Game
from player import AIPlayer, RandomPlayer, PartlyAIPlayer
from recorder import record_games
from train_data_loader import generate_replayable_games


def __get_player(t, i):
    if t == "m":
        return AIPlayer("[{}] AI".format(i))
    elif t == "r":
        return RandomPlayer("[{}] Random Player".format(i))
    elif t == "mr":
        return PartlyAIPlayer("[{}] Partly AI Player".format(i))

    raise Exception("Invalid Player Type: {}!".format(t))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p1", help="Player 1 - m = Trained Model, r = Player random, mr = Player random/ai")
    parser.add_argument("-p2", help="Player 2 - m = Trained Model, r = Player random, mr = Player random/ai")
    parser.add_argument("-r", help="Rounds to play - Number")
    args = parser.parse_args()

    p1 = __get_player(args.p1, 1)
    p2 = __get_player(args.p2, 2)
    r = int(args.r)

    games = []
    p1_wins = 0
    p2_wins = 0
    ties_as_second_player = 0
    ties_total = 0

    for i in range(r):
        g = Game(p1, p2, show_game=False)
        winner = g.run()

        if winner == -1:
            # TIE
            ties_total += 1
            if isinstance(p2,AIPlayer):
                ties_as_second_player += 1
        elif winner == 0:
            p1_wins += 1
        elif winner == 1:
            p2_wins += 1

        games.append(g)

    file_name = record_games(games)

    print("\nRESULTS ({}):".format(r))
    print("P1 Wins: {}".format(p1_wins))
    print("P2 Wins: {}".format(p2_wins))
    print("TIES (TOTAL): {}".format(ties_total))
    print("TIES (AI as second player): {}".format(ties_as_second_player))
