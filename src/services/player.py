import random
import src.repo.player_repo as r
import src.domain.player as d
import src.services.board as b
import os

class PlayerServices():
    def __init__(self, player_repo: r.PlayerRepo, board_services:b.BoardServices):
        self._repo = player_repo
        self._bserv = board_services
        # AI data
        self._last_x = 0
        self._last_y = 0
        self._current_x = 0
        self._current_y = 0
        self._direction = 0

    def make_move_computer_hard(self, player_id, opponent_id):
        # Computer will play in the following way:
        # It picks 2 random coordinates. If it hits a ship, then it will search and destroy the whole ship before it decides to make another move.
        player = self._repo.get_player(player_id) # computer
        opponent = self._repo.get_player(opponent_id) # human
        player_dummy_board = player.get_opp_board()
        opp_board = opponent.get_board()
        x = random.randint(1, 10)
        y = random.randint(1, 10)

        result = self._bserv.make_move(opp_board, x, y)
        if result == 0:  # missed
            player_dummy_board.set_cell(x, y, "O")
        elif result == 1:  # hit a ship
            player_dummy_board.set_cell(x, y, "X")
            ship = opp_board.get_ship(x, y)
            self._bserv.destroy_ship(opp_board, ship) # destroy the entire ship
            self._bserv.cover_ship(opp_board, ship)

            self._bserv.destroy_ship(player_dummy_board, ship) # mark result on the dummy board (not necessary for computer player)
            self._bserv.cover_ship(player_dummy_board, ship)

        return result

    def make_move_computer_easy(self, player_id, opponent_id, x = 0, y = 0):
        # Computer will play in the following way:
        # It picks 2 random coordinates. If it hits a ship, then it will try to hit it again in a randomnly chosen direction.
        player = self._repo.get_player(player_id) # computer
        opponent = self._repo.get_player(opponent_id) # human
        opp_board = opponent.get_board()
        if x == 0 or y == 0:
            x = random.randint(1, 10)
            y = random.randint(1, 10)

        result = self._bserv.make_move(opp_board, x, y)
        if result == 1:  # hit a ship
            direction = [-1, 1]
            ship = opp_board.get_ship(x, y)

            # If ship has been completely destroyed, mark it on computer's map and search for another
            if self._bserv.check_ship(opp_board, ship) == 1:
                self._bserv.cover_ship(opp_board, ship)

            else:
                # Randomly pick a direction for next attack
                direct = random.choice(direction)
                if ship.vertical == 1:
                    x += direct
                    if x < 1:
                        x += 2
                    if x > 10:
                        x -= 2
                else:
                    y += direct
                    if y < 1:
                        y += 2
                    if y > 10:
                        y -= 2

                self.make_move_computer_easy(player_id, opponent_id, x, y)
                return 0

        return result

    def search_ship(self, player_id, opponent_id, ship):
        player = self._repo.get_player(player_id)  # computer
        opponent = self._repo.get_player(opponent_id)  # human
        opp_board = opponent.get_board()

        if ship.vertical == 1:
            self._current_x += self._direction
        else:
            self._current_y += self._direction

        # don't make move outside board
        if self._current_x < 1 or self._current_x > 10 or self._current_y < 1 or self._current_y > 10:
            return -1

        result = self._bserv.make_move(opp_board, self._current_x, self._current_y)
        return result

    def make_move_computer_normal(self, player_id, opponent_id):
        # Computer will play in the following way:
        # It picks 2 random coordinates. If it hits a ship, then it will try to hit it again in a randomnly chosen direction.
        # Compared to the easy algorithm, this time the computer does not forget the last ship it attacked until it is destroyed.

        player = self._repo.get_player(player_id) # computer
        opponent = self._repo.get_player(opponent_id) # human
        opp_board = opponent.get_board()

        if self._last_x == 0 or self._last_y == 0:
            x = random.randint(1, 10)
            y = random.randint(1, 10)
        else:
            x = self._current_x
            y = self._current_y

        if self._direction == 0:
            direction = [-1, 1]
            self._direction = random.choice(direction)

        if x < 1 or x > 10 or y < 1 or y > 10:
            self._last_x, self._last_y = (0, 0)
            self._direction = 0
            return -1

        result = self._bserv.make_move(opp_board, x, y)
        if result == 1:  # hit a ship
            ship = opp_board.get_ship(x, y)
            (self._last_x, self._last_y) = (x, y)
            # If ship has been completely destroyed, mark it on computer's map and search for another
            if self._bserv.check_ship(opp_board, ship) == 1:

                self._bserv.cover_ship(opp_board, ship)
                self._last_x, self._last_y = (0, 0)
                self._direction = 0

            else:
                # If ship is hit, save coordinates of last successful strike
                self._current_x, self._current_y = (x, y)

                # Search the ship in one direction until it cannot be attacked
                while self.search_ship(player_id, opponent_id, ship) == 1:
                    pass

                # Once the search is done, resume the coordinates to the first strike and search in the opposite direction (second search is done next turn)
                self._direction *= -1
                if ship.vertical == 1:
                    self._last_x += self._direction
                else:
                    self._last_y += self._direction
                self._current_x, self._current_y = (self._last_x, self._last_y)

                # End turn
                return 0

        # -1 is returned when a move was already made; since it cannot make a move, reset coordinates and randomly pick 2 other
        if result == -1:
            self._last_x, self._last_y = (0, 0)
            self._direction = 0

        return result


    def make_move_human(self, player_id, opponent_id, x, y):
        player = self._repo.get_player(player_id) # human
        opponent = self._repo.get_player(opponent_id) # computer
        player_dummy_board = player.get_opp_board()
        opp_board = opponent.get_board()

        # Make move on opponent's board and then modify the player's dummy board
        result = self._bserv.make_move(opp_board, x, y)
        if result == 0: # missed
            player_dummy_board.set_cell(x, y, "O")
        elif result == 1: # hit a ship
            player_dummy_board.set_cell(x, y, "X")
            if self._bserv.check_ship(opp_board, opp_board.get_ship(x, y)) == 1:
                self._bserv.cover_ship(player_dummy_board, opp_board.get_ship(x, y))
        return result

