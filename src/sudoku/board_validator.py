def validate_board(board):
    size = len(board)
    box_size = int(size ** 0.5)

    def is_unique(nums):
        nums = [n for n in nums if n != 0]
        return len(nums) == len(set(nums))

    for i in range(size):
        if not is_unique(board[i]) or not is_unique([board[j][i] for j in range(size)]):
            return False

    for box_row in range(0, size, box_size):
        for box_col in range(0, size, box_size):
            box = [
                board[i][j]
                for i in range(box_row, box_row + box_size)
                for j in range(box_col, box_col + box_size)
            ]
            if not is_unique(box):
                return False

    return True