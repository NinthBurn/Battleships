import src.domain.ship as s
import src.domain.board as b
import src.domain.player as p
import unittest as t
import board_repo as br
import player_repo as pr

class TestRepository(t.TestCase):
    def board_test(self):
        # Create 2 boards and a repository
        new_board = b.Board(1)
        new_board2 = b.Board(2)
        REPO = br.BoardRepo()

        # Add them and check if they are registered in the repository
        REPO.add_board(new_board)
        REPO.add_board(new_board2)
        self.assertIn(new_board, REPO.get_boards())
        self.assertIn(new_board2, REPO.get_boards())

        # Initialize all the boards and then check if they are empty
        REPO.initialize_boards()
        test_board = b.Board(0)
        test_board.initialize_board()
        self.assertEqual(str(REPO.get_board(1)), str(test_board))
        self.assertEqual(str(REPO.get_board(2)), str(test_board))

        # Remove a board and check that it has been deleted from repository
        REPO.remove_board(2)
        self.assertNotIn(new_board2, REPO.get_boards())


    def player_test(self):
        # Create 2 player instances and the repository
        board_player = b.Board(1)
        board_opponent = b.Board(2)
        player = p.Player(1, 2, board_player, board_opponent)
        opponent = p.Player(2, 1, board_opponent, board_player)
        REPO = pr.PlayerRepo()

        # Add them and check if they are registered in the repository
        REPO.add_player(player)
        REPO.add_player(opponent)
        self.assertEqual(player, REPO.get_player(1))
        self.assertEqual(opponent, REPO.get_player(2))

        # Remove a player and check that it has been deleted from repository
        REPO.remove_player(1)
        self.assertNotIn(player, REPO.get_players())


    def test_all(self):
        self.board_test()
        self.player_test()

if __name__ == "__main__":
    test_case = TestRepository
    test_case.test_all()
