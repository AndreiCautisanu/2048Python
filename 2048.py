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
# we only need to implement this one function instead of one for each direction, due to the fact that we can move in all other directions
# by rotating the board matrix around in our move methods and sliding to the left
# e.g. moving up is just rotating the board counter-clockwise, sliding the tiles to the left, and rotating the board matrix back

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



# same rationale applies to the merging function, which will only merge equal numbered tiles as if we had just moved left
# we can apply the merge function on the rotated board matrix when we want to move up, down or right, as i've explained before the slide_left function

def merge(board):

    new_board = board

    for row_i in range(4):
        for col_i in range(3):
            if new_board[row_i][col_i] == new_board[row_i][col_i + 1] and new_board[row_i][col_i] != 0:
                new_board[row_i][col_i] *= 2
                new_board[row_i][col_i + 1] = 0

    return slide_left(new_board)  # slide again to cover empty spaces






if __name__ == "__main__":
    board = np.array([[2, 2, 4, 0], [8, 8, 0, 2], [2, 4, 0, 4], [0, 4, 0, 2]])
    board = slide_left(board)
    print(board)
    board = merge(board)
    print(board)