import src.domain.player as p

class PlayerRepo:
    def __init__(self):
        self._players = {}

    def add_player(self, player:p.Player):
        player_id = player._player_id
        if player_id in self._players.keys():
            raise p.PlayerException("Player already exists.")

        self._players[player_id] = player

    def remove_player(self, player_id):
        if player_id not in self._players.keys():
            raise p.PlayerException("Player does not exist.")

        self._players.pop(player_id)

    def get_player(self, player_id):
        if player_id not in self._players.keys():
            raise p.PlayerException("Player does not exist.")

        return self._players[player_id]

    def get_players(self):
        return list(self._players.values())