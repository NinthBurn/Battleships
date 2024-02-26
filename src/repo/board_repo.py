import src.domain.board as b

class BoardRepo:
    def __init__(self):
        self._board_list = {}

    def add_board(self, board):
        if board.get_id() in self._board_list.keys():
            raise b.BoardException("Board already exists.")

        self._board_list[board.get_id()] = board

    def remove_board(self, board_id):
        if board_id not in self._board_list.keys():
            raise b.BoardException("Board does not exist.")

        self._board_list.pop(board_id)

    def get_board(self, board_id):
        if board_id not in self._board_list.keys():
            raise b.BoardException("Board does not exist.")

        return self._board_list[board_id]

    def get_boards(self):
        return list(self._board_list.values())

    def initialize_boards(self):
        for board_id in self._board_list.keys():
            self._board_list[board_id].initialize_board()