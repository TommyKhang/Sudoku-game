import random

class HintSystem:
    def __init__(self, board, solved_board, hints_left=3):
        self.board = board
        self.solved_board = solved_board
        self.hints_left = hints_left

    def find_empty_cells(self):
        return [(i, j) for i in range(len(self.board)) for j in range(len(self.board[i])) if self.board[i][j] == 0]

    def provide_random_hint(self):
        if self.hints_left <= 0:
            return None

        empty_cells = self.find_empty_cells()
        if not empty_cells:
            return None

        row, col = random.choice(empty_cells)
        value = self.solved_board[row][col]

        self.board[row][col] = value
        self.hints_left -= 1

        return row, col, value
