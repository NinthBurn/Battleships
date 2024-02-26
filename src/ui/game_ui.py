import src.domain.player as pdom
import src.domain.board as bdom
import src.repo.board_repo as brepo
import src.repo.player_repo as prepo
import src.services.board as bserv
import src.services.player as pserv

from texttable import Texttable

class UIException(Exception):
    def __init__(self, msg):
        self.error = msg

    def __str__(self):
        return self.error

class GameUI:
    def __init__(self, BOARDREPO: brepo.BoardRepo, BOARDSERV: bserv.BoardServices, PLAYERREPO: prepo.PlayerRepo, PLAYERSERV: pserv.PlayerServices):
        self._brepo = BOARDREPO
        self._bserv = BOARDSERV
        self._prepo = PLAYERREPO
        self._pserv = PLAYERSERV
        self._rows = 10
        self._cols = 10
        self.make_move_computer = self._pserv.make_move_computer_easy

    def print_commands(self):
        print("help - display all commands")
        print("quit/exit - exit the program")
        print("attack XY - attack opponent at specified coordinates")

    def translate_coordinates(self, coordinates):
        # Coordinates are given in string form, and this functions translates them into a pair of 2 integers.
        # Ex: B4 - first element is a letter, second is a digit. Also accepts lower case letters.
        if len(coordinates) < 2 or len(coordinates) > 3:
            raise UIException("Invalid coordinates.")
        coordinates = coordinates.upper()
        letters = [ 'A', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        if len(coordinates) == 3:
             int_str = coordinates[1] + coordinates[2]
             x = int(int_str)
        else:
            x = int(coordinates[1])

        if coordinates[0] not in letters or x < 1 or x > 10:
            raise UIException("Invalid coordinates.")

        for y in range(1, 11):
            if letters[y] == coordinates[0]:
                break
        return (x, y)

    def process_command(self, command):
        command = command.split(" ")
        if command[0] == "quit" or command[0] == "exit":
            print("Closing game.")
            return 0 # close game

        elif command[0] == "attack":
            coordinates = self.translate_coordinates(command[1])
            move_result = self._pserv.make_move_human(0, 1, coordinates[0], coordinates[1])
            if move_result == -1:
                print("You cannot make the same move twice.")
                return 2 # continue turn
            if move_result == 1:
                return 2

        elif command[0] == "help":
            self.print_commands()
            return 3 # continue turn

        elif command[0] == "computerarea":
            print("~~~ Computer's game board ~~~")
            self.print_boards(self._prepo.get_player(1)) # CHEAT - show computer's board
            return 2 # continue turn

        else:
            raise UIException("Invalid command. Please try again.")
        return 1 # move to next turn

    def print_boards(self, Player:pdom.Player):
        # Print the player's board and the opponent's dummy board next to it.
        t = Texttable()
        header = ["X"]
        board_player = (Player.get_board()).get_elements()  # Player's board
        board_opponent = (Player.get_opp_board()).get_elements()  # Opponent "dummy" board
        width = []
        for i in range(25):
            width.append(2)
        t.set_cols_width(width)
        for ascii in range(self._cols):
            header.append(chr(65 + ascii))

        for spaces in range(4):
            header.append(' ')

        for ascii in range(self._cols):
            header.append(chr(65 + ascii))

        t.header(header)
        t.set_cols_width(width)
        for r in range(1, self._rows+1):
            column = []
            for c in range(1, self._cols+1):
                column.append(board_player[r][c])

            for c in range(4):
                column.append('##')

            for c in range(1, self._cols + 1):
                column.append(board_opponent[r][c])

            t.add_row([r] + column)

        return print(t.draw())


    def run_ui(self):
        self.main()
        player_turn = True
        keep_running = True
        human_player = self._prepo.get_player(0)
        computer_player = self._prepo.get_player(1)
        self.print_boards(human_player)

        while keep_running == True:
            try:
                if self._bserv.check_board(human_player.get_board()) == 0:
                    print("Game over! Computer wins.")
                    keep_running = False
                    break
                if self._bserv.check_board(computer_player.get_board()) == 0:
                    print("You win!")
                    keep_running = False
                    break

                if player_turn == True:
                    command = input(">")
                    result = self.process_command(command)
                    if result == 0:
                        keep_running = False
                        return
                    if result == 2:
                        self.print_boards(human_player)
                        continue
                    if result == 3:
                        continue
                    player_turn = not player_turn
                else:
                    result = self.make_move_computer(1, 0)
                    if result == 0:
                        player_turn = not player_turn

                self.print_boards(human_player)
            except Exception as e:
                print(e)

    def main(self):
        # Prepare boards for players
        player_board = bdom.Board(1)
        player_dummy_board = bdom.Board(2)
        computer_board = bdom.Board(3)
        computer_dummy_board = bdom.Board(4)

        # Add them to the repo
        self._brepo.add_board(player_board)
        self._brepo.add_board(player_dummy_board)
        self._brepo.add_board(computer_board)
        self._brepo.add_board(computer_dummy_board)

        # Prepare the boards for the game
        self._brepo.initialize_boards()
        player_board = self._bserv.generate_board_classic(player_board)
        computer_board = self._bserv.generate_board_classic(computer_board)

        # Generate players and save the instances
        human_player = pdom.Player(0, 1, player_board, player_dummy_board)
        computer_player = pdom.Player(1, 0, computer_board, computer_dummy_board)
        self._prepo.add_player(human_player)
        self._prepo.add_player(computer_player)



# initiate game data
BOARDREPO = brepo.BoardRepo()
BOARDSERV = bserv.BoardServices(BOARDREPO)
PLAYERREPO = prepo.PlayerRepo()
PLAYERSERV = pserv.PlayerServices(PLAYERREPO, BOARDSERV)
game_ui = GameUI(BOARDREPO, BOARDSERV, PLAYERREPO, PLAYERSERV)

# start
game_ui.run_ui()