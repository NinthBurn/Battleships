class PlayerException(Exception):
    def __init__(self, msg):
        self.error = msg

    def __str__(self):
        return self.error

class Player:
    def __init__(self, player_id, opponent_id, player_board, opponent_board):
        self._player_id = player_id
        self._opponent_id = opponent_id
        self._player_board = player_board
        self._opponent_board = opponent_board

    def get_id(self):
        return self._player_id

    def get_opp_id(self):
        return self._opponent_id

    def get_board(self):
        return self._player_board

    def get_opp_board(self):
        return self._opponent_board
