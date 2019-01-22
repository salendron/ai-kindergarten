from google.cloud import datastore
import json, datetime
import numpy as np


def generate_alternate_situations():
    client = datastore.Client.from_service_account_json(
        'ds_identity.json'
    )

    last_train_date = None

    key = datastore.key.Key('LastTraining', 1, project="ai-kindergarten")
    saved_entity = client.get(key)

    if saved_entity is not None:
        last_train_date = saved_entity['timestamp']

    query = client.query(kind='Game')
    query.add_filter('winner', '=', 'h')

    if last_train_date is not None:
        query.add_filter('timestamp', '>', last_train_date)

    games = list(query.fetch())

    x_data = []
    y_data = []
    for game in games:
        moves = game['moves']
        states = json.loads(game['states'])

        right_move = moves[-1]
        last_state = states[-3]

        x_data.append(last_state)
        y_data.append(right_move)

    return x_data, y_data


def get_games():
    client = datastore.Client.from_service_account_json(
        'ds_identity.json'
    )

    last_train_date = None

    key = datastore.key.Key('LastTraining', 1, project="ai-kindergarten")
    saved_entity = client.get(key)

    if saved_entity is not None:
        last_train_date = saved_entity['timestamp']

    query = client.query(kind='Game')

    if last_train_date is not None:
        query.add_filter('timestamp', '>', last_train_date)

    games = list(query.fetch())

    x_data = []
    y_data = []
    for game in games:
        winner = game['winner']
        moves = game['moves']
        states = json.loads(game['states'])
        players = game['players']

        if winner == 'h' or winner == 'm':
            winner_id = players.index(winner)
            winner_moves = [moves[i] for i in range(len(moves)) if i % 2 == winner_id]
            winner_states = [states[i] for i in range(len(states)) if i % 2 == winner_id]

            x_data += winner_states
            y_data += winner_moves
        elif winner == 't': #a tie means second player wins
            winner_moves = [moves[i] for i in range(len(moves)) if i % 2 == 1]
            winner_states = [states[i] for i in range(len(states)) if i % 2 == 1][:-1]

            x_data += winner_states
            y_data += winner_moves

    x_alternate, y_alternate = generate_alternate_situations()
    x_data += x_alternate
    y_data += y_alternate

    x_train = np.array(x_data[0:int(len(x_data) / 2)])
    y_train = np.array(y_data[0:int(len(y_data) / 2)])

    x_test = np.array(x_data[int(len(x_data) / 2):])
    y_test = np.array(y_data[int(len(y_data) / 2):])

    return x_train, y_train, x_test, y_test


def save_last_training():
    client = datastore.Client.from_service_account_json(
        'ds_identity.json'
    )

    key = datastore.key.Key('LastTraining', 1, project="ai-kindergarten")

    saved_entity = client.get(key)

    if saved_entity is None:
        saved_entity = datastore.Entity(key=key)

        saved_entity.update({
            'timestamp':datetime.datetime.now()
        })

        client.put(saved_entity)
    else:
        saved_entity.update({
            'timestamp':datetime.datetime.now()
        })

        client.put(saved_entity)