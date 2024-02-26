import src.domain.player as pdom
import src.domain.board as bdom
import src.repo.board_repo as brepo
import src.repo.player_repo as prepo
import src.services.board as bserv
import src.services.player as pserv

import random
import pygame
import src.ui.highlightbutton as button
from sys import exit

class GameUI:
    def __init__(self, BOARDREPO: brepo.BoardRepo, BOARDSERV: bserv.BoardServices, PLAYERREPO: prepo.PlayerRepo, PLAYERSERV: pserv.PlayerServices):
        self._brepo = BOARDREPO
        self._bserv = BOARDSERV
        self._prepo = PLAYERREPO
        self._pserv = PLAYERSERV
        self._rows = 10
        self._cols = 10

        pygame.init()

        # load player data
        self.generate_board = self.select_gamemode()
        self.initiate_players()
        self.human_player = self._prepo.get_player(0)
        self.computer_player = self._prepo.get_player(1)
        self.make_move_computer = self.select_difficulty()

        # window WxH
        # 1440 x 720
        self._width = 1440
        self._height = 720
        self._frames = 60 # FPS
        self._waterframecount = 0
        self._WIN = pygame.display.set_mode((self._width, self._height))

        pygame.display.set_caption("Battleships")

        # cell & table details
            # Something to note: the screen is divided in 30x15 cells of size 48px for scaling purposes.

        self._cell_size = 48
        self._player_table_x = 96
        self._opp_table_x = 768
        self._table_y = 48

        # graphics definition
        self.SHIP_PART = pygame.image.load('resources/materials/ship_part.png')
        self.SHIP_PART = pygame.transform.scale_by(self.SHIP_PART, 1.5)
        self.SHIP_HIT = pygame.image.load('resources/materials/hit_part.png')
        self.SHIP_HIT = pygame.transform.scale_by(self.SHIP_HIT, 1.5)
        self.EMPTYCELL = pygame.image.load('resources/materials/empty.png')
        self.EMPTYCELL = pygame.transform.scale_by(self.EMPTYCELL, 3)
        self.BORDER = pygame.image.load('resources/materials/border.png')
        self.BORDER = pygame.transform.scale_by(self.BORDER, 1.5)
        self.CELLBORDER = pygame.image.load('resources/materials/cell_border.png')
        self.CELLBORDER = pygame.transform.scale_by(self.CELLBORDER, 1.5)
        self.CELLSELECT = pygame.image.load('resources/materials/cell_selected.png')
        self.CELLSELECT = pygame.transform.scale_by(self.CELLSELECT, 1.5)
        self.EXITBUTTON = pygame.image.load('resources/materials/exit_button.png')
        self.EXITBUTTON = pygame.transform.scale_by(self.EXITBUTTON, 1.5)
        self.EXITPROMPT = pygame.image.load('resources/materials/exit_prompt.png')
        self.EXITPROMPT = pygame.transform.scale_by(self.EXITPROMPT, 4 )
        self.BUTTONHOVER = pygame.image.load('resources/materials/button_press.png')
        self.BUTTONHOVER = pygame.transform.scale_by(self.BUTTONHOVER, 4)
        self.BACKGROUND = pygame.image.load('resources/materials/background.jpg')
        self.FAILPIC = pygame.image.load('resources/materials/fail.png')
        self.FAILPIC = pygame.transform.scale_by(self.FAILPIC, 4)
        self.WINPIC = pygame.image.load('resources/materials/winner.png')
        self.WINPIC = pygame.transform.scale_by(self.WINPIC, 4)

        self.MISSLIST = []
        for i in range(1, 9):
            filename = 'resources/materials/miss' + str(i) + '.png'
            self.MISSLIST.append(pygame.image.load(filename))
            self.MISSLIST[i - 1] = pygame.transform.scale_by(self.MISSLIST[i - 1], 1.5)
        self.MISS = self.MISSLIST

        # music and sound
        music_path = 'resources/sound/COMBAT0' + str(random.randint(1, 4)) + '.mp3'
        self.MUSIC = pygame.mixer.music.load(music_path)
        self.SPLASH = pygame.mixer.Sound('resources/sound/splash.mp3')
        self.EXPLOSION = pygame.mixer.Sound('resources/sound/explosion.mp3')
        pygame.mixer.music.play(-1)

    def select_difficulty(self):
        import os
        if not os.path.exists("difficulty.txt"):
            fp = open("difficulty.txt", "w")
            fp.write("easy\n\neasy | normal | hard")
            return self._pserv.make_move_computer_easy

        fp = open("difficulty.txt", "r")
        lines = fp.readlines()
        for difficulty in lines:
            print(difficulty)
            if difficulty == 'normal\n' or difficulty == 'normal':
                return self._pserv.make_move_computer_normal
            elif difficulty == 'hard\n' or difficulty == 'hard':
                return self._pserv.make_move_computer_hard
            else:
                return self._pserv.make_move_computer_easy

    def select_gamemode(self):
        import os
        if not os.path.exists("gamemode.txt"):
            fp = open("gamemode.txt", "w")
            fp.write("classic\n\nclassic | russian")
            return self._bserv.generate_board_classic

        fp = open("gamemode.txt", "r")
        lines = fp.readlines()
        for gamemode in lines:
            print(gamemode)
            if gamemode == 'russian\n' or gamemode == 'russian':
                return self._bserv.generate_board_russian
            else:
                return self._bserv.generate_board_classic

    def display_cell(self, game_board: bdom.Board, cell_template, cell_x, cell_y):
        # Displays the proper graphic depending on the data from player's table.
        # Requires the player for access to the board, as well as the coordinates of the cell (cell_x and cell_y).

        # animated water texture :D
        if self._waterframecount > self._frames:
            self._waterframecount = 0
        self._waterframecount += 0.01

        cell = game_board.get_cell(cell_x, cell_y)
        if cell == '#':
            self._WIN.blit(self.SHIP_PART, (cell_template.x, cell_template.y))

        elif cell == 'X':
            self._WIN.blit(self.SHIP_HIT, (cell_template.x, cell_template.y))

        elif cell == 'O':
            self._WIN.blit(self.MISS[int(self._waterframecount) // 8], (cell_template.x, cell_template.y))

        else:
            self._WIN.blit(self.EMPTYCELL, (cell_template.x, cell_template.y))

    def draw_borders(self):
        # Horizontal border
        for i in range(0, 12):
            # Upper border - player
            x_coord = self._player_table_x + i * self._cell_size
            y_coord = self._table_y
            self._WIN.blit(self.BORDER, (x_coord, y_coord))

            # Lower border - player
            y_coord = self._table_y + self._cell_size * 11
            self._WIN.blit(self.BORDER, (x_coord, y_coord))

            # Upper border - opponent
            x_coord = self._opp_table_x + i * self._cell_size
            y_coord = self._table_y
            self._WIN.blit(self.BORDER, (x_coord, y_coord))

            # Lower border - opponent
            y_coord = self._table_y + self._cell_size * 11
            self._WIN.blit(self.BORDER, (x_coord, y_coord))

        # Vertical border
        for i in range(1, 11):
            # Left border - player
            x_coord = self._player_table_x
            y_coord = self._table_y + i * self._cell_size
            self._WIN.blit(self.BORDER, (x_coord, y_coord))

            # Right border - player
            x_coord = self._player_table_x + self._cell_size * 11
            self._WIN.blit(self.BORDER, (x_coord, y_coord))

            # Left border - opponent
            x_coord = self._opp_table_x
            self._WIN.blit(self.BORDER, (x_coord, y_coord))

            # Right border - opponent
            x_coord = self._opp_table_x + self._cell_size * 11
            self._WIN.blit(self.BORDER, (x_coord, y_coord))

        for i in range(1, 11):
            for j in range(1, 11):
                x_coord = self._player_table_x + i * self._cell_size
                y_coord = self._table_y + j * self._cell_size
                self._WIN.blit(self.CELLBORDER, (x_coord, y_coord))

                x_coord = self._opp_table_x + i * self._cell_size
                self._WIN.blit(self.CELLBORDER, (x_coord, y_coord))

    def draw_cells(self, game_board: bdom.Board, offset_x):
        for i in range(1, self._rows + 1):
            for j in range(1, self._cols + 1):

                cell = pygame.Rect(self._player_table_x + i * self._cell_size + offset_x, self._table_y + j * self._cell_size,
                                   self._cell_size, self._cell_size)
                self.display_cell(game_board, cell, j, i)

    def draw_boards(self, player: pdom.Player):
        # Draw cells of player's board
        board = player.get_board()
        self.draw_cells(board, 0)

        # Draw cells of opponent's board
        board = player.get_opp_board()
        self.draw_cells(board, 14*self._cell_size)

        # Draw borders
        self.draw_borders()

    def draw_window(self):

        self._WIN.blit(self.BACKGROUND, (0, 0))
        self.draw_boards(self.human_player)
        self._WIN.blit(self.EXITBUTTON, (0, 0))
        # pygame.display.update()

    def initiate_players(self):
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
        player_board = self.generate_board(player_board)
        computer_board = self.generate_board(computer_board)

        # Generate players and save the instances
        human_player = pdom.Player(0, 1, player_board, player_dummy_board)
        computer_player = pdom.Player(1, 0, computer_board, computer_dummy_board)
        self._prepo.add_player(human_player)
        self._prepo.add_player(computer_player)

    def hover_over_cell(self):
        current_cell = pygame.math.Vector2(pygame.mouse.get_pos()) // self._cell_size
        col = int(current_cell[0])
        row = int(current_cell[1])

        # Check if cursor is inside a table - horizontal check
        if not (current_cell[0] == 0 and current_cell[1] == 0):  # exit button
            if (current_cell[0] < 3 or current_cell[0] > 12) and (current_cell[0] < 17 or current_cell[0] > 26):
                return

            # Check if cursor is inside a table - vertical check
            if current_cell[1] < 2 or current_cell[1] > 11:
                return

        idk = button.HighlightButton(self._player_table_x + (col - 2) * self._cell_size,
                                     self._table_y + (row - 1) * self._cell_size, self.CELLSELECT)

        idk.draw(self._WIN)

        return
        # Displays a nice border if player is hovering over a cell.
        current_cell = pygame.math.Vector2(pygame.mouse.get_pos()) // self._cell_size

        # Check if cursor is inside a table - horizontal check
        if not (current_cell[0] == 0 and current_cell[1] == 0): # exit button
            if (current_cell[0] < 3 or current_cell[0] > 12) and (current_cell[0] < 17 or current_cell[0] > 26):
                return

            # Check if cursor is inside a table - vertical check
            if current_cell[1] < 2 or current_cell[1] > 11:
                return

        col = int(current_cell[0]) * 48
        row = int(current_cell[1]) * 48
        self._WIN.blit(self.CELLSELECT, (col, row))

    def exit_menu(self):
        exitp_x, exitp_y = (464, 264)
        self._WIN.blit(self.EXITPROMPT, (exitp_x, exitp_y))
        exit_button = button.HighlightButton(exitp_x + 64, exitp_y + 64, self.BUTTONHOVER)
        dont_exit_button = button.HighlightButton(exitp_x + 64 + 256, exitp_y + 64, self.BUTTONHOVER)
        if exit_button.draw(self._WIN):
            pygame.quit()
            exit()
            return True

        if dont_exit_button.draw(self._WIN):
            return False
        return True

    def make_player_move(self, x, y):
        move_result = self._pserv.make_move_human(0, 1, y, x)
        return move_result

    def play_sound(self, sound_num):
        # Play appropriate sound depending on player action.
        if sound_num == 0:
            self.SPLASH.play()
        if sound_num == 1:
            self.EXPLOSION.play()

    def player_input(self, exit_pressed):
        # Returns two values: PLAYER_TURN_VALUE, EXIT_PRESSED_VALUE
        # Returns True if player can still continue his turn | If exit button has been pressed.
        # Returns False if player's turn is over | False otherwise
        if exit_pressed:
            exit_pressed = self.exit_menu()

        else:
            self.hover_over_cell()

            current_cell = pygame.math.Vector2(pygame.mouse.get_pos()) // self._cell_size
            col = int(current_cell[0])
            row = int(current_cell[1])

            left_click = pygame.mouse.get_pressed()[0]  # 0 - left click, 1 - right click
            if left_click == True:
                if col == 0 and row == 0:
                    exit_pressed = True
                    self.exit_menu()

                # Check if player clicked inside attacking board
                if (col > 16 and col < 27) and (row > 1 and row < 12):
                    result = self.make_player_move(col - 16, row - 1)
                    self.play_sound(result)
                    if result == 0:
                        return False, exit_pressed

        return True, exit_pressed

    def check_win_loss_condition(self):
        # Returns True if game is over; False otherwise
        # Check if player lost
        # exitp_x, exitp_y = (656 - 64, 328 - 32) this was for 2x
        exitp_x, exitp_y = (464, 264)
        if self._bserv.check_board(self.human_player.get_board()) == 0:
            self._WIN.blit(self.FAILPIC, (exitp_x, exitp_y))
            return True

        # Check if player won
        if self._bserv.check_board(self.computer_player.get_board()) == 0:
            self._WIN.blit(self.WINPIC, (exitp_x, exitp_y))
            return True

        return False

    def pygame_event_check(self):
        # Needed for every loop or the game freezes
        keep_running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_running = False
                pygame.quit()
                exit()
            if event.type == pygame.VIDEORESIZE:
                self._WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        return keep_running

    def game_over_menu(self):
        # exitp_x, exitp_y = (688, 374) this was for 2x
        exitp_x, exitp_y = (672, 400)
        keep_running = True
        while keep_running:
            exit_button = button.HighlightButton(exitp_x, exitp_y, self.EMPTYCELL)
            pygame.display.update()
            keep_running = self.pygame_event_check()
            keep_running = not exit_button.draw(self._WIN)

    def main(self):
        clock = pygame.time.Clock()
        keep_running = True
        exit_pressed = False
        player_turn = True

        while keep_running:
            clock.tick(self._frames)
            self.draw_window()

            # Check for losing or winning condition
            if self.check_win_loss_condition():
                keep_running = False
                break

            if player_turn: # Human player turn
                player_turn, exit_pressed = self.player_input(exit_pressed)
            else: # Computer player turn
                result = self.make_move_computer(1, 0)
                # self.play_sound(result)
                if result == 0:
                    player_turn = not player_turn

            # pygame event stuff
            pygame.display.update()
            keep_running = self.pygame_event_check()


        self.game_over_menu()
        pygame.quit()


# initiate game data
BOARDREPO = brepo.BoardRepo()
BOARDSERV = bserv.BoardServices(BOARDREPO)
PLAYERREPO = prepo.PlayerRepo()
PLAYERSERV = pserv.PlayerServices(PLAYERREPO, BOARDSERV)

# start
game_ui = GameUI(BOARDREPO, BOARDSERV, PLAYERREPO, PLAYERSERV)
game_ui.main()

