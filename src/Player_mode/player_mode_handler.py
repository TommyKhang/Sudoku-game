from src.Player_mode.hint_system import HintSystem

class SudokuPlayerMode:
    def __init__(self, board_generator, board_solver):
        self.board_generator = board_generator
        self.board_solver = board_solver
        self.current_board = []
        self.solved_board = []
        self.hint_system = None
        self.score = 0
        self.checks_used = 0
        self.hints_used = 0

    def generate_puzzle(self, difficulty):
        self.reset_score()
        self.current_board = self.board_generator(difficulty)
        self.solved_board = self.board_solver([row[:] for row in self.current_board])
        self.hint_system = HintSystem(self.current_board, self.solved_board, hints_left=3)

        if difficulty == "medium":
            self.checks_left = 15
        elif difficulty == "hard":
            self.checks_left = 10
        else:
            self.checks_left = 0
        return self.current_board

    def use_hint(self):
        if self.hint_system:
            hint = self.hint_system.provide_random_hint()
            if hint:
                self.hints_used += 1
                return hint
        return None

    def validate_move(self, row, col, value):
        return self.solved_board[row][col] == value

    def check_move(self, row, col, value):
        self.checks_used += 1
        return self.solved_board[row][col] == value

    def reset_score(self):
        self.score = 0
        self.checks_used = 0
        self.hints_used = 0

    def update_score_for_complete(self):
        correct_cells = 0
        for i in range(len(self.current_board)):
            for j in range(len(self.current_board[i])):
                if self.current_board[i][j] == self.solved_board[i][j]:
                    correct_cells += 1

        self.score += correct_cells * 20

        self.score -= self.hints_used * 10
        self.score -= self.checks_used * 5

    def update_score_for_hint(self):
        self.score -= 10

    def update_score_for_check(self):
        self.score -= 5

    def is_game_complete(self):
        return self.current_board == self.solved_board