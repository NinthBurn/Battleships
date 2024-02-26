import src.domain.ship as s

class BoardException(Exception):
    def __init__(self, msg):
        self.error = msg

    def __str__(self):
        return self.error

class Board:
    def __init__(self, board_id):
        self.__board = []
        self.__board_id = board_id
        self.cols = 12
        self.rows = 12
        self._ships = {}

    def get_elements(self):
        return self.__board

    def __str__(self):
        result_str = ""
        for row in self.__board:
            row_str = ""
            for cell in row:
                row_str += cell
            result_str += row_str + "\n"
        return result_str

    def initialize_board(self):
        self.__board = [[' ' for i in range(self.cols)] for j in range(self.rows)]

    def get_id(self):
        return self.__board_id

    def get_cell(self, x, y):
        """
        x, y - coordinates
        Returns the value of cell given by coordinates x and y.
        """
        return self.__board[x][y]

    def set_cell(self, x, y, value):
        """
        x, y - coordinates
        Sets value for cell found at coordinates (x,y)
        """
        self.__board[x][y] = value

    def create_ship(self, x, y, size, vertical):
        # Creates a ship and saves it to the board.
        ship = s.Battleship(x, y, size, vertical)
        ship_coords = (x, y)
        self._ships[ship_coords] = ship

    def get_ship(self, x, y):
        ship_coords = (x, y)
        if ship_coords not in self._ships.keys():
            raise BoardException("There is no ship at specified coordinates.")

        return self._ships[ship_coords]

    def register_ship(self, ship: s.Battleship):
        # Establishes a reference between cells on the board and the ship located on those cells.
        x = ship.x
        y = ship.y
        if ship.vertical == 1:
            for i in range(x, x + ship.size):
                ship_coords = (i, y)
                self._ships[ship_coords] = ship
        else:
            for i in range(y, y + ship.size):
                ship_coords = (x, i)
                self._ships[ship_coords] = ship