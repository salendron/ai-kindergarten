import datetime, json

DT_FORMAT = "%Y-%m-%d_%H-%M-%S"
TRAIN_DATA_PATH = './train_data/'


def record_games(games):
    data_timestamp = datetime.datetime.now().strftime(DT_FORMAT)
    file_name = "{}_games.json".format(data_timestamp)

    data = {"games": []}

    for g in games:
        data["games"].append(g.states)

    with open(TRAIN_DATA_PATH + file_name, 'w') as outfile:
        json.dump(data, outfile)

    return file_name