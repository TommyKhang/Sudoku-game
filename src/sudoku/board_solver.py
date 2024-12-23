from .utils import is_valid

def solve_sudoku(board):
    size = len(board)

    def solve():
        for row in range(size):
            for col in range(size):
                if board[row][col] == 0:
                    for num in range(1, size + 1):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if solve():
                                return True
                            board[row][col] = 0
                    return False
        return True

    return board if solve() else None