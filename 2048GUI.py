import tkinter as tk
from tkinter import messagebox
from random import choices
import numpy as np
import boardFunctions

COLORS = {
    'bg_app': '#a6bdbb',
    'text': '#776e65',
    0:    '#8eaba8',
    2:    '#eee4da',
    4:    '#ede0c8',
    8:    '#f2b179',
    16:   '#f59563',
    32:   '#f675cf',
    64:   '#f65e3b',
    128:  '#edcf72',
    256:  '#edcc61',
    512:  '#edc850',
    1024: '#edc53f',
    2048: '#edc22e'
}

FONT = ('Helvetica', 44, 'bold')

class Game(tk.Frame):
    
    def __init__(self):
        tk.Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.maxsize(650, 625)
        self.master.minsize(650, 625)

        self.cells = []  # holds the tk labels inside the board matrix tiles
        self.build_board()
        self.redraw()
        self.master.bind("<Key>", self.key_pressed)
        print("draw")

        self.mainloop()


    # function that builds the initial board cells and background
    def build_board(self):

        self.init_board()

        background = tk.Frame(self, bg = COLORS['bg_app'], width = 600, height = 600)
        background.grid()

        for row_i in range(4):
            grid_row = []
            for col_i in range(4):

                # make cell blocks
                cell = tk.Frame(background, bg = COLORS[0], width = 100, height = 100)

                # equal padding on all sides
                cell.grid(
                            row = row_i, column = col_i, 
                            padx = (10, 5) if col_i == 0 else 5 if col_i != 3 else (5, 10), 
                            pady = (10, 5) if row_i == 0 else 5 if row_i != 3 else (5, 10)
                )

                # add cell labels to hold the numbers and add them to the cell array to modify with the redraw function
                cell_label = tk.Label(cell, text = "", bg = COLORS[0], justify = tk.CENTER, font = FONT, width = 4, height = 2)
                cell_label.grid()
                grid_row.append(cell_label)
            
            self.cells.append(grid_row)


    # function to redraw the numbers on the board corresponding to the stored board matrix - go through all the cell labels and update them according to the corresponding
    # value inside the board matrix
    def redraw(self):
        for row_i in range(4):
            for col_i in range(4):
                val = self.board[row_i][col_i]
                
                if val > 0:
                    self.cells[row_i][col_i].configure(text = str(val), bg = COLORS.get(val, '#000000'), fg = COLORS['text'])
                else:
                    self.cells[row_i][col_i].configure(text = "", bg = COLORS[0])

        


    #function gets called on each key press event, manipulates the board if player presses WASD
    def key_pressed(self, event):
        key = repr(event.char)
        key_moves = {
            "'w'": self.player_move_up,
            "'a'": self.player_move_left,
            "'s'": self.player_move_down,
            "'d'": self.player_move_right
        }
        if key in ["'w'", "'a'", "'s'", "'d'"]:
            flag = key_moves[key]()
            if flag == True:
                self.add_new_tile()
                self.redraw()


        # check if the game is over
        if self.gameWon():
            response = messagebox.showinfo('You win!', 'Congratulations, you got 2048!')
            if response == 'ok':
                self.destroy()
                self.quit()

        if not self.movePossible():
            response = messagebox.showinfo('You lose!', 'You can no longer make a legal move, you\'ve lost!')
            if response == 'ok':
                self.destroy()
                self.quit()

        self.update_idletasks()



# BOARD MANIPULATION FUNCTIONS


    # function that initializes the starting board
    def init_board(self):
        self.board = np.zeros((4,4), dtype=int)

        rng = np.random.default_rng()
        twos_placed = 0

        # game starts with two 2 tiles on random positions
        while twos_placed < 2:
            two_coords = rng.integers(0, 4, 2)
            if self.board[two_coords[0]][two_coords[1]] == 0:
                self.board[two_coords[0]][two_coords[1]] = 2
                twos_placed += 1



    # function that slides all tiles to the left
    # we only need to implement this one function instead of one for each direction, due to the fact that we can move in all other directions
    # by rotating the board matrix around in our move methods and sliding to the left
    # e.g. moving up is just rotating the board counter-clockwise, sliding the tiles to the left, and rotating the board matrix back
    def slide_board_left(self):

        new_board = np.zeros((4,4), dtype=int)
        flag = False
        i = 0

        for row in self.board:
            arr = list(row[row != 0])                           # get tiles in row that are not empty
            empty_spaces_no = 4 - len(arr)                      # create an array of zeros equal to the number of empty spaces on the row
            zeros = [0 for i in range(empty_spaces_no)]
            new_row = arr + zeros                               # concatenate the two arrays
            new_board[i] = new_row

            compare = row == new_row
            rows_equal = compare.all()                          # this checks if the original row is equal to the new row

            if not rows_equal:
                flag = True                                     # new row different from original row, so slide was possible

            i += 1

        self.board = new_board
        return flag

    
    # same rationale applies to the merging function, which will only merge equal numbered tiles as if we had just moved left
    # we can apply the merge function on the rotated board matrix when we want to move up, down or right, as i've explained before the slide_board_left function

    def merge_board_pieces(self):

        new_board = np.copy(self.board)
        flag = False

        for row_i in range(4):
            for col_i in range(3):
                if new_board[row_i][col_i] == new_board[row_i][col_i + 1] and new_board[row_i][col_i] != 0:
                    new_board[row_i][col_i] *= 2                # double the leftmost square in the equal pair
                    new_board[row_i][col_i + 1] = 0             # remove the other one
                    flag = True

        self.board = new_board
        _ = self.slide_board_left() # slide everything to the left again to cover empty spaces

        return flag



    # function to add a new numbered tile on a random position
    def add_new_tile(self):

        # get all empty spaces in board matrix
        free_positions = np.argwhere(self.board == 0)

        # new tile has an 80% chance of being a 2 and a 20% chance of being a 4
        new_tile_val = choices([2, 4], [0.8, 0.2])[0]
        new_tile_pos = free_positions[np.random.randint(0, len(free_positions))]

        self.board[new_tile_pos[0]][new_tile_pos[1]] = new_tile_val


    # function for moving up, rotate board counter-clockwise once, slide and merge to the left, rotate it back
    def player_move_up(self):
        self.board = np.rot90(self.board)
        flag_slide_success = self.slide_board_left()
        flag_merge_success = self.merge_board_pieces()

        flag_move_success = flag_slide_success or flag_merge_success

        self.board = np.rot90(self.board, -1)
        return flag_move_success


    # function for moving down, rotate board clockwise once, slide and merge to the left, rotate it back
    def player_move_down(self):
        self.board = np.rot90(self.board, -1)
        flag_slide_success = self.slide_board_left()
        flag_merge_success = self.merge_board_pieces()

        flag_move_success = flag_slide_success or flag_merge_success

        self.board = np.rot90(self.board)
        return flag_move_success


    # function for moving left, no rotation necessary
    def player_move_left(self):
        flag_slide_success = self.slide_board_left()
        flag_merge_success = self.merge_board_pieces()

        flag_move_success = flag_slide_success or flag_merge_success

        return flag_move_success


    # function for moving right, rotate board twice, slide and merge to the left, rotate it back
    def player_move_right(self):
        self.board = np.rot90(self.board, 2)
        flag_slide_success = self.slide_board_left()
        flag_merge_success = self.merge_board_pieces()

        flag_move_success = flag_slide_success or flag_merge_success

        self.board = np.rot90(self.board, -2)
        return flag_move_success


    #check if there is any possible move by checking if there are any adjacent same-numbered tile pairs or if there is any single tile left
    def movePossible(self):
        if 0 in self.board:
            return True

        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0 and (self.board[i][j] == self.board[i][j+1] or self.board[i][j] == self.board[i+1][j]):
                    return True

        return False

    def gameWon(self):
        return 2048 in self.board

game_grid = Game()