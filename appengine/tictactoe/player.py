import random
import googleapiclient.discovery
import numpy as np


class RandomPlayer(object):

    def get_move(self,game):
        return random.choice(game.get_valid_moves())


class AIPlayer(object):

    def predict(self, project, model, instances, version=None):
        # Create the ML Engine service object.
        # To authenticate set the environment variable
        # GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_file>
        service = googleapiclient.discovery.build('ml', 'v1', cache_discovery=False)

        name = 'projects/{}/models/{}'.format(project, model)

        if version is not None:
            name += '/versions/{}'.format(version)

        response = service.projects().predict(
            name=name,
            body={'instances': instances}
        ).execute()

        if 'error' in response:
            raise RuntimeError(response['error'])

        return response['predictions']

    def get_move(self,game):
        predictions = self.predict("ai-kindergarten", "tictactoe", [game.states[-1], ])
        move = np.argmax(predictions[0]['output'])

        valid_moves = game.get_valid_moves()
        if move in valid_moves:
            print("AI MOVE: {}".format(move))
            return move

        print("Invalid move: {}".format(move))
        return random.choice(game.get_valid_moves())
