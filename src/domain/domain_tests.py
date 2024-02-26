import ship as s
import board as b
import player as p
import unittest as t

class TestDomain(t.TestCase):
    def ship_test(self):
        # Create a battleship
        new_ship = s.Battleship(1, 1, 4, 0)
        new_ship2 = s.Battleship(2, 2, 1, 0)

        # Check that data has been registered correctly
        self.assertEqual(new_ship.x, 1)
        self.assertEqual(new_ship.y, 1)
        self.assertEqual(new_ship.size, 4)
        self.assertEqual(new_ship.vertical, 0)

        self.assertEqual(new_ship2.x, 2)
        self.assertEqual(new_ship2.y, 2)
        self.assertEqual(new_ship2.size, 1)
        self.assertEqual(new_ship2.vertical, 0)

        # Check that the 2 ships are different entities
        self.assertNotEqual(new_ship, new_ship2)

    def board_test(self):
        # Create a board and initialize it
        new_board = b.Board(1)
        new_board.initialize_board()

        test_board = [[' ' for i in range(12)] for j in range(12)]

        # Check ID
        self.assertEqual(new_board.get_id(), 1)
        # Check if new_board has been initialized to the empty board
        self.assertEqual(test_board, new_board.get_elements())

        # Test create_ship and get_ship functions
        new_board.create_ship(1, 1, 4, 0)
        new_ship = s.Battleship(1, 1, 4, 0)
        self.assertEqual(new_ship, new_board.get_ship(1, 1))

        # Test set_cell and get_cell functions
        new_board.set_cell(5, 4, "T")
        self.assertEqual("T", new_board.get_cell(5, 4))

        # Test register_ship function
        new_board.register_ship(new_ship)
        self.assertEqual(new_ship, new_board.get_ship(1, 3))

    def player_test(self):
        board_player = b.Board(1)
        board_opponent = b.Board(2)
        player = p.Player(1, 2, board_player, board_opponent)
        opponent = p.Player(2, 1, board_opponent, board_player)

        # Get IDs
        self.assertEqual(player.get_id(), 1)
        self.assertEqual(opponent.get_id(), 2)
        self.assertEqual(player.get_opp_id(), 2)
        self.assertEqual(opponent.get_opp_id(), 1)

        # Get boards
        self.assertEqual(player.get_opp_board(), opponent.get_board())
        self.assertEqual(player.get_board(), opponent.get_opp_board())

    def test_all(self):
        self.board_test()
        self.ship_test()
        self.player_test()

if __name__ == "__main__":
    test_case = TestDomain
    test_case.test_all()