import math

def is_valid(board, row, col, num):
    size = len(board)
    box_size = int(math.sqrt(size))
    for i in range(size):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_row, box_col = row - row % box_size, col - col % box_size
    for i in range(box_row, box_row + box_size):
        for j in range(box_col, box_col + box_size):
            if board[i][j] == num:
                return False
    return True