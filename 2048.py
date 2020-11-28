import numpy as np


# function that initializes and returns the starting board
def init_board():
    board = np.zeros((4,4), dtype=int)

    rng = np.random.default_rng()
    twos_placed = 0

    while twos_placed < 2:
        two_coords = rng.integers(0, 4, 2)
        if board[two_coords[0]][two_coords[1]] == 0:
            board[two_coords[0]][two_coords[1]] = 2
            twos_placed += 1

    print(board)

    return board





# function that slides all tiles to the left
# we only need to implement this one function instead of one for each direction, thanks to the fact that we can move in all other directions
# by flipping the board matrix around in different ways in our move methods

def slide_left(board):

    new_board = np.zeros((4,4), dtype=int)
    i = 0

    for row in board:
        arr = list(row[row != 0])                           # get tiles in row that are not empty
        empty_spaces_no = 4 - len(arr)                      # create an array of zeros equal to the number of empty spaces on the row
        zeros = [0 for i in range(empty_spaces_no)]
        new_row = arr + zeros                               # concatenate the two arrays
        new_board[i] = new_row
        i += 1

    
    return new_board



if __name__ == "__main__":
    board = np.array([[0, 2, 2, 0], [0, 0, 0, 4], [0, 2, 4, 4], [0, 4, 0, 2]])
    print(slide_left(board))