from google.cloud import datastore
from config import ENV
import datetime, json


def get_ds_client():
    return datastore.Client()


def save_stats(winner):
    h = 0 if winner != 'h' else 1
    m = 0 if winner != 'm' else 1
    t = 0 if winner != 't' else 1

    client = get_ds_client()

    key = datastore.key.Key('Stats', 1, project="ai-kindergarten")

    saved_entity = client.get(key)

    if saved_entity is None:
        saved_entity = datastore.Entity(key=key)

        saved_entity.update({
            'h': h,
            'm': m,
            't': t,
        })

        client.put(saved_entity)
    else:
        saved_entity.update({
            'h': saved_entity['h'] + h,
            'm': saved_entity['m'] + m,
            't': saved_entity['t'] + t,
        })

        client.put(saved_entity)


def get_stats():
    client = get_ds_client()

    key = datastore.key.Key('Stats', 1, project="ai-kindergarten")

    saved_entity = client.get(key)
    if saved_entity is None:
        return 0, 0, 0
    else:
        return saved_entity['h'], saved_entity['m'], saved_entity['t']


def get_last_training():
    client = get_ds_client()

    key = datastore.key.Key('LastTraining', 1, project="ai-kindergarten")

    saved_entity = client.get(key)

    if saved_entity is None:
        return "Never"
    else:
        return saved_entity['timestamp'].strftime('%d, %b %Y at %H:%M')


def save_game(game):
    client = get_ds_client()

    winner = game.get_winner()
    winner_id = 'i' #incomplete game
    if winner == 2: #tie
        winner_id = 't'
    else:
        winner_id = game.players[winner] # h or m

    entity = datastore.Entity(key=client.key('Game'))
    entity.update({
        'timestamp':datetime.datetime.now(),
        'players': game.players,
        'current-player': game.current_player,
        'states': json.dumps(game.states),
        'moves': game.moves,
        'winner':winner_id
    })
    client.put(entity)

    save_stats(winner_id)



