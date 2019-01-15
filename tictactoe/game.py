from copy import deepcopy


def get_move_by_states(from_state, to_state):
    for i in range(len(from_state)):
        if from_state[i] != to_state[i]:
            return i


class Game(object):

    def __init__(self, player1, player2, show_game=False):
        self.show_game = show_game
        self.players = [player1, player2]
        self.current_player = 0
        self.states = []
        self.moves = []

        #generate empty board
        self.states.append(
            [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        )

    def restore(self,states,rewind=0):
        for i in  range(len(states) - (1 + rewind)):
            move = get_move_by_states(states[i], states[i + 1])
            self.__play(move)
            self.current_player = 1 if self.current_player == 0 else 0

    def play_move(self,move):
        self.__play(move)
        self.current_player = 1 if self.current_player == 0 else 0

    def _is_valid_move(self,move):
        try:
            move = int(move)
        except ValueError:
            return False

        if move < 0 or move > 8:
            return False

        if move not in self.get_valid_moves():
            return False

        return True

    def get_valid_moves(self):
        current_state = self.states[-1]

        valid_moves = []
        for i in range(9):
            if current_state[i] == -1:
                valid_moves.append(i)

        return valid_moves

    def __play(self,move):
        if not self._is_valid_move(move):
            raise Exception("Invalid move!")

        move = int(move)

        new_state = deepcopy(self.states[-1])
        new_state[move] = self.current_player

        self.states.append(new_state)
        self.moves.append(move)

    def __next_move(self):
        player = self.players[self.current_player]

        move = player.get_move(self)

        self.__play(move)

        self.current_player = 1 if self.current_player == 0 else 0

    def print_board(self):
        if self.show_game:
            current_state = self.states[-1]

            board_str = "\n"
            for f in range(9):
                if f != 0 and f % 3 == 0:
                    board_str += "\n"
                elif f != 0:
                    board_str += " "

                if current_state[f] == 0:
                    board_str += "X"
                elif current_state[f] == 1:
                    board_str += "O"
                else:
                    board_str += "_"

            print(board_str)

    def get_winner(self):
        current_state = self.states[-1]

        #check each player
        for p in range(2):

            # check each row
            for r in range(3):
                f1 = r * 3
                if current_state[f1] == p and current_state[f1 + 1] == p and current_state[f1 + 2] == p:
                    return p

            # check each column
            for c in range(3):
                if current_state[c] == p and current_state[c + 3] == p and current_state[c + 6] == p:
                    return p

            # check diagonal
            if current_state[0] == p and current_state[4] == p and current_state[8] == p:
                return p

            if current_state[2] == p and current_state[4] == p and current_state[6] == p:
                return p

        # check for a tie
        moves_played = 0
        for f in current_state:
            if f != -1:
                moves_played += 1

        if moves_played == 9:
            return -1

        return None

    def run(self):
        winner = None
        while winner is None:
            self.print_board()
            self.__next_move()

            winner = self.get_winner()

        self.print_board()
        return winner