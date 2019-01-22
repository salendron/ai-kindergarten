from bottle import SimpleTemplate
from bottle import request
from .game import Game
from .player import AIPlayer
from .recorder import save_game, get_stats, get_last_training

player_names = {
    'm': 'Bob',
    'h': 'You'
}


def render_field(idx, game):
    current_state = game.states[-1]

    if current_state[idx] == -1:
        return -1
    elif current_state[idx] == 0:
        return 0
    else:
        return 1


def index():
    token = request.forms.get('game_token')
    game = Game.from_token(token)

    winner = -1

    move = request.forms.get('move')

    if move is not None:
        game.play(int(move))
        winner = game.get_winner()

        if winner == -1:
            game.play(AIPlayer().get_move(game))
            winner = game.get_winner()

    if token is None and game.players[0] == 'm':
        # first round and bob has the first move
        game.play(AIPlayer().get_move(game))

    if winner != -1:
        save_game(game)

    #load stats
    stats_h, stats_m, stats_t = get_stats()

    tpl = SimpleTemplate(name="index.tpl", lookup=['./static/web/'])
    return tpl.render(
        content='tictactoe',
        token=game.to_token(),
        winner=winner,
        player0=player_names[game.players[0]],
        player1=player_names[game.players[1]],
        winner_name=player_names[game.players[winner]] if winner != -1 and winner != 2 else "",
        stats_h=stats_h,
        stats_m=stats_m,
        stats_t=stats_t,
        last_train=get_last_training(),
        field0=render_field(0, game),
        field1=render_field(1, game),
        field2=render_field(2, game),
        field3=render_field(3, game),
        field4=render_field(4, game),
        field5=render_field(5, game),
        field6=render_field(6, game),
        field7=render_field(7, game),
        field8=render_field(8, game)
    )


