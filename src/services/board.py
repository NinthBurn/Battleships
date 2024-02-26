import src.domain.board as d # domain
import src.repo.board_repo as r # repo
import src.domain.ship as s
import random
import copy

class BoardServices:
    def __init__(self, repository:r.BoardRepo):
        self._repo = repository
        self._repo.initialize_boards()
        self._limit = 10 # limit size of board
        self.part = '#'

    def check_board(self, board: d.Board):
        # Returns 1 if there are ships not completely destroyed. Returns 0 if all ships have been destroyed.
        for i in range(1, 11):
            for j in range(1, 11):
                if board.get_cell(i, j) == self.part:
                    return 1
        return 0

    def make_move(self, board: d.Board, x:int, y:int):
        # Registers a move on the board and returns a value according to the result.
        # -1 : move has been already registered
        # 0 : missed
        # 1 : hit
        if x < 0 or y < 0 or x > self._limit or y > self._limit:
            raise d.BoardException("Coordinates are outside of board.")

        current_cell = board.get_cell(x, y)
        if current_cell == 'X' or current_cell == 'O':
            return -1 # move already registered
        if current_cell == " ":
            board.set_cell(x, y, 'O')
            return 0 # missed
        if current_cell == self.part:
            board.set_cell(x, y, 'X')
            self.cover_ship(board, board.get_ship(x, y))
            return 1 # hit

    def check_area(self, board: d.Board, ship: s.Battleship):
        """
        Checks if there are no ships that conflict with the one passed as parameter.
        Returns 0 if no conflicts were found, -1 otherwise.
        """
        x = ship.x
        y = ship.y
        size = ship.size
        vertical = ship.vertical
        if vertical == 1:
            for i in range(x-1, x+size+1):
                for j in range(y-1, y+2):
                    if board.get_cell(i,j) != " ":
                        return -1
        else:
            for i in range(x-1, x+2):
                for j in range(y-1, y+size+1):
                    if board.get_cell(i,j) != " ":
                        return -1
        return 0

    def add_ship(self, board: d.Board, ship: s.Battleship):
        """
        Adds a ship of specified size to the board, starting from coordinates x and y (if possible).
        """
        x = ship.x
        y = ship.y
        size = ship.size
        vertical = ship.vertical
        if x + size - 1 > self._limit or y + size - 1 > self._limit:
            raise d.BoardException("Ship does not fit!")
        if self.check_area(board, ship) == -1:
            raise d.BoardException("Ship is in conflict with other ships and cannot be placed!")

        # Create a link between ship and board
        board.create_ship(x, y, size, vertical)
        board.register_ship(ship)

        if vertical == 1:
            for i in range(x, x+size):
                board.set_cell(i, y, self.part)
        else:
            for i in range(y, y+size):
                board.set_cell(x, i, self.part)

    def destroy_ship(self, board: d.Board, ship: s.Battleship):
        # Used by the AI to provide a challenge to the player. If it touches a ship, it gets completely destroyed.
        x = ship.x
        y = ship.y
        size = ship.size
        if ship.vertical == 1:
            for i in range(x, x + size):
                board.set_cell(i, y, 'X')
        else:
            for i in range(y, y + size):
                board.set_cell(x, i, 'X')

    def check_ship(self, board: d.Board, ship: s.Battleship):
        # Checks whether or not a ship has been completely destroyed. Returns 1 if it is, 0 otherwise.
        x = ship.x
        y = ship.y
        size = ship.size
        if ship.vertical == 1:
            for i in range(x, x + size):
                if board.get_cell(i, y) == self.part:
                    return 0
        else:
            for i in range(y, y + size):
                if board.get_cell(x, i) == self.part:
                    return 0
        return 1

    def cover_ship(self, board: d.Board, ship: s.Battleship):
        # If a ship gets completed destroyed, mark surrounding area as already visited (since there can't be any other ship in that area).
        if self.check_ship(board, ship) == 0:
            return
        x = ship.x
        y = ship.y
        size = ship.size
        if ship.vertical == 1:
            for i in range(x - 1, x + size + 1):
                for j in range(y - 1, y + 2):
                    if board.get_cell(i, j) == " ":
                        board.set_cell(i, j, 'O')
        else:
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + size + 1):
                    if board.get_cell(i, j) == " ":
                        board.set_cell(i, j, 'O')

    def generate_board_classic(self, current_board):
        """
        Generates a valid configuration of 5 ships for a given board.
        Function returns the resulted game board.
        """
        sizes = [5, 4, 3, 3, 2]
        # Carrier = #####
        # Battleship = ####
        # Cruiser = ###
        # Destroyer = ##
        for ship in range(0, 5):
            generated = False
            while not generated:
                try:
                    temp_board = copy.deepcopy(current_board) # make a copy of the configuration generated so far
                    vertical = random.randint(0,1)
                    # The optimal interval for random coordinates would be (1,7); higher number require more tries before a valid config is generated
                    x = random.randint(1,10)
                    y = random.randint(1,10)
                    current_ship = s.Battleship(x, y, sizes[ship], vertical)

                    self.add_ship(temp_board, current_ship)
                    generated = True
                    current_board = temp_board
                except: # keep trying until a valid configuration has been generated
                    generated = False

        return current_board

    def generate_board_russian(self, current_board):
        """
        Generates a valid configuration of 9 ships for a given board.
        Function returns the resulted game board.
        """
        sizes = [4, 3, 3, 2, 2, 1, 1, 1, 1]
        for ship in range(0, 9):
            generated = False
            while not generated:
                try:
                    temp_board = copy.deepcopy(current_board) # make a copy of the configuration generated so far
                    vertical = random.randint(0,1)
                    # The optimal interval for random coordinates would be (1,7); higher number require more tries before a valid config is generated
                    x = random.randint(1,10)
                    y = random.randint(1,10)
                    current_ship = s.Battleship(x, y, sizes[ship], vertical)

                    self.add_ship(temp_board, current_ship)
                    generated = True
                    current_board = temp_board
                except: # keep trying until a valid configuration has been generated
                    generated = False

        return current_board
