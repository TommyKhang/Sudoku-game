class SudokuPlayerMode:
    def __init__(self, board_generator, board_solver):
        self.board_generator = board_generator
        self.board_solver = board_solver
        self.current_board = []
        self.solved_board = []
        self.hints_left = 3

    def generate_puzzle(self, difficulty):
        self.current_board = self.board_generator(difficulty)
        self.solved_board = self.board_solver([row[:] for row in self.current_board])
        self.hints_left = 3
        return self.current_board

    def use_hint(self):
        if self.hints_left <= 0:
            return None

        empty_cells = [
            (i, j) for i in range(len(self.current_board)) for j in range(len(self.current_board[i]))
            if self.current_board[i][j] == 0
        ]

        if not empty_cells:
            return None

        row, col = empty_cells[0]  # Take the first empty cell
        value = self.solved_board[row][col]
        self.current_board[row][col] = value
        self.hints_left -= 1
        return row, col, value

    def validate_move(self, row, col, value):
        return self.solved_board[row][col] == value

    def is_game_complete(self):

        return self.current_board == self.solved_board


# Example usage:
if __name__ == "__main__":
    from src.sudoku.board_generator import generate_puzzle
    from src.sudoku.board_solver import solve_sudoku

    player_mode = SudokuPlayerMode(generate_puzzle, solve_sudoku)
    board = player_mode.generate_puzzle("easy")

    print("Generated Board:")
    for row in board:
        print(row)

    print("\nUsing a hint:")
    hint = player_mode.use_hint()
    if hint:
        print(f"Hint: Row {hint[0]}, Col {hint[1]}, Value {hint[2]}")

    print("\nBoard After Hint:")
    for row in player_mode.current_board:
        print(row)

    print("\nIs game complete?", player_mode.is_game_complete())