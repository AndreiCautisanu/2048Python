import numpy as np


#function that initializes and returns the starting board
def init():
    board = np.zeros((4,4), dtype=int)

    rng = np.random.default_rng()
    twos_placed = 0

    while twos_placed < 2:
        two_coords = rng.integers(0, 4, 2)
        if board[two_coords[0]][two_coords[1]] == 0:
            board[two_coords[0]][two_coords[1]] = 2
            twos_placed += 1

    print(board)

if __name__ == "__main__":
    init()