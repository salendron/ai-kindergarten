from game import Game

def get_winner_by_game_state(final_state):
    g = Game(None,None)
    g.states.append(final_state)
    winner = g.get_winner()

    if winner is None: #incomplete game
        fields_played = 0
        for f in final_state:
            if f != -1:
                fields_played += 1

        winner = 1 if fields_played % 2 == 0 else 0

    return winner