### Updated Code for All Modules ###

import random
from .utils import is_valid

# Define valid board sizes for consistency
VALID_SIZES = [4, 9, 16]

# Generate a fully solved Sudoku board

def generate_board(size=9):
    """
    Generate a fully solved Sudoku board of the specified size.
    """
    if size not in VALID_SIZES:
        raise ValueError(f"Invalid board size. Supported sizes are {VALID_SIZES}.")

    board = [[0] * size for _ in range(size)]

    def fill_board(board):
        for row in range(size):
            for col in range(size):
                if board[row][col] == 0:
                    nums = list(range(1, size + 1))
                    random.shuffle(nums)
                    for num in nums:
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if fill_board(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    fill_board(board)
    return board

# Remove cells to create a puzzle

def remove_cells(board, num_cells):
    """
    Remove the specified number of cells from the board to create a puzzle.
    """
    cells = [(i, j) for i in range(len(board)) for j in range(len(board))]
    random.shuffle(cells)
    for i, j in cells[:num_cells]:
        board[i][j] = 0
    return board

# Generate a Sudoku puzzle based on difficulty level

def generate_puzzle(difficulty):
    """
    Generate a Sudoku puzzle of the given difficulty level.
    """
    DIFFICULTY_REMOVAL = {'easy': 35, 'medium': 45, 'hard': 55}
    num_cells_to_remove = DIFFICULTY_REMOVAL.get(difficulty, 35)
    solved_board = generate_board()
    return remove_cells(solved_board, num_cells_to_remove)

# Generate a random board (not guaranteed to be solvable)

def generate_random_board(size):
    """
    Generate a random Sudoku board of the specified size.
    This board is not guaranteed to be solvable.
    """
    if size not in VALID_SIZES:
        raise ValueError(f"Invalid board size. Supported sizes are {VALID_SIZES}.")

    board = [[0] * size for _ in range(size)]
    for row in range(size):
        for col in range(size):
            nums = list(range(1, size + 1))
            random.shuffle(nums)
            for num in nums:
                if is_valid(board, row, col, num):
                    board[row][col] = num
                    break
    return board
