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
    flag = False
    i = 0

    for row in board:
        arr = list(row[row != 0])                           # get tiles in row that are not empty
        empty_spaces_no = 4 - len(arr)                      # create an array of zeros equal to the number of empty spaces on the row
        zeros = [0 for i in range(empty_spaces_no)]
        new_row = arr + zeros                               # concatenate the two arrays
        new_board[i] = new_row

        compare = row == new_row
        rows_equal = compare.all()

        if not rows_equal:
            flag = True                                     # new row different from original row, so slide was possible

        i += 1

    
    return (new_board, flag)



# same rationale applies to the merging function, which will only merge equal numbered tiles as if we had just moved left
# we can apply the merge function on the rotated board matrix when we want to move up, down or right, as i've explained before the slide_left function

def merge(board):

    new_board = np.copy(board)
    flag = False

    for row_i in range(4):
        for col_i in range(3):
            if new_board[row_i][col_i] == new_board[row_i][col_i + 1] and new_board[row_i][col_i] != 0:
                new_board[row_i][col_i] *= 2
                new_board[row_i][col_i + 1] = 0
                flag = True

    slide_board, _ = slide_left(new_board)

    return slide_board, flag  # slide again to cover empty spaces



# function to add a new numbered tile on a random position
# new tiles have an 80% chance of being a 2, and a 20% chance of being a 4

def add_new_tile(board):
    free_positions = []

    for row_i in range(len(board)):
        for col_i in range(len(board[row_i])):
            if board[row_i][col_i] == 0:
                free_positions.append((row_i, col_i))
    
    
    new_tile_distribution = [4, 4, 2, 2, 2, 2, 2, 2, 2, 2]
    new_tile_val = new_tile_distribution[np.random.randint(0, len(new_tile_distribution))]
    new_tile_pos = free_positions[np.random.randint(0, len(free_positions))]

    board[new_tile_pos[0]][new_tile_pos[1]] = new_tile_val

    return board





# function for moving up, rotate board counter-clockwise once, slide and merge to the left, rotate it back
def player_move_up(board):
    board = np.rot90(board)
    board, flag_slide_success = slide_left(board)
    board, flag_merge_success = merge(board)
    flag_move_success = flag_slide_success or flag_merge_success

    original_board = np.rot90(board, -1)
    return (original_board, flag_move_success)


# function for moving down, rotate board clockwise once, slide and merge to the left, rotate it back
def player_move_down(board):
    board = np.rot90(board, -1)
    board, flag_slide_success = slide_left(board)
    board, flag_merge_success = merge(board)
    flag_move_success = flag_slide_success or flag_merge_success

    original_board = np.rot90(board)
    return (original_board, flag_move_success)


# function for moving left, no rotation necessary
def player_move_left(board):
    board, flag_slide_success = slide_left(board)
    board, flag_merge_success = merge(board)
    flag_move_success = flag_slide_success or flag_merge_success

    return (board, flag_move_success)


# function for moving right, rotate board twice, slide and merge to the left, rotate it back
def player_move_right(board):
    board = np.rot90(board, 2)
    board, flag_slide_success = slide_left(board)
    board, flag_merge_success = merge(board)
    flag_move_success = flag_slide_success or flag_merge_success
    original_board = np.rot90(board, -2)
    return (original_board, flag_move_success)


def player_move(board, direction):
    if direction == 'w':
        board = np.rot90(board)
        board, flag_slide_success = slide_left(board)
        board, flag_merge_success = merge(board)
        flag_move_success = flag_slide_success or flag_merge_success

        original_board = np.rot90(board, -1)
        return (original_board, flag_move_success)

    elif direction == 's':
        board = np.rot90(board, -1)
        board, flag_slide_success = slide_left(board)
        board, flag_merge_success = merge(board)
        flag_move_success = flag_slide_success or flag_merge_success

        original_board = np.rot90(board)
        return (original_board, flag_move_success)

    elif direction == 'a':
        board, flag_slide_success = slide_left(board)
        board, flag_merge_success = merge(board)
        flag_move_success = flag_slide_success or flag_merge_success

        return (board, flag_move_success)

    elif direction == 'd':
        board = np.rot90(board, 2)
        board, flag_slide_success = slide_left(board)
        board, flag_merge_success = merge(board)
        flag_move_success = flag_slide_success or flag_merge_success
        original_board = np.rot90(board, -2)
        return (original_board, flag_move_success)

    else:
        return (board, False)




# TODO - add checks to see if the move actually happens (if there is any space at all), do not complete the move and do not add a new tile if the move is impossible


if __name__ == "__main__":
    # board = np.array([[2, 2, 4, 0], [8, 8, 0, 2], [2, 4, 0, 4], [0, 4, 0, 2]])
    # board = slide_left(board)
    # print(board)
    # board = merge(board)
    # print(board)

    # board = add_new_tile(board)
    # print(board)

    board = np.array([[2, 2, 4, 0], [2, 0, 4, 0], [0, 0, 2, 0], [0, 0, 2, 0]])
    print(board)
    board, flag = player_move_up(board)
    print(board)

    print("---")

    board = np.array([[2, 2, 0, 0], [4, 0, 0, 0], [8, 2, 0, 2], [8, 0, 0, 2]])
    print(board)
    board, flag = player_move_down(board)
    print(board)

    print("---")

    board = np.array([[2, 0, 0, 0], [2, 0, 0, 0], [2, 0, 0, 0], [2, 0, 0, 0]])
    print(board)
    board, flag = player_move_left(board)
    print(board)
    print(flag)

