import tkinter as tk
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


FONTS = {
    '2XL': ('Helvetica', 72, 'bold'),
    'XL':  ('Helvetica', 60, 'bold'),
    'L':   ('Helvetica', 44, 'bold'),
    'M':   ('Helvetica', 32, 'bold'),
    'S':   ('Helvetica', 24, 'bold')
}


class Game(tk.Frame):
    
    def __init__(self):
        tk.Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.maxsize(650, 625)
        self.master.minsize(650, 625)

        self.cells = []
        self.build_board()
        self.redraw()
        self.master.bind("<Key>", self.key_pressed)
        print("draw")

        self.mainloop()


    # function that builds the initial board cells and background
    def build_board(self):

        self.board = boardFunctions.init_board()

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
                            pady = (10, 5) if row_i == 0 else 5 if row_i != 3 else (5, 10))

                # add cell labels to hold the numbers and add them to the cell array to modify with the redraw function
                cell_label = tk.Label(cell, text = "", bg = COLORS[0], justify = tk.CENTER, font = FONTS['L'], width = 4, height = 2)
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
                    self.cells[row_i][col_i].configure(text = str(val), bg = COLORS[val], fg = COLORS['text'])
                else:
                    self.cells[row_i][col_i].configure(text = "", bg = COLORS[0])

        self.update_idletasks()


    def key_pressed(self, event):
        key = repr(event.char)

        key_moves = {
            "'w'": boardFunctions.player_move_up,
            "'a'": boardFunctions.player_move_left,
            "'s'": boardFunctions.player_move_down,
            "'d'": boardFunctions.player_move_right
        }
        if key in ["'w'", "'a'", "'s'", "'d'"]:
            self.board, flag = key_moves[key](self.board)
            if flag == True:
                self.board = boardFunctions.add_new_tile(self.board)
                self.redraw()


game_grid = Game()