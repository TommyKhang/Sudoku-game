import tkinter as tk
from tkinter import messagebox
from src.Player_mode.player_mode_handler import SudokuPlayerMode
from src.sudoku.board_generator import generate_puzzle, generate_random_board
from src.sudoku.board_solver import solve_sudoku
from .widgets import RoundedButton

class ModernSudokuApp:
    def __init__(self):
        self.hint_button = None
        self.score_label = None
        self.size_entry = None
        self.entries = None
        self.player_mode = SudokuPlayerMode(generate_puzzle, solve_sudoku)
        self.root = tk.Tk()
        self.root.title("Sudoku")
        self.root.geometry("600x800")
        self.current_board = []
        self.hints_left = 3

        # Configure colors and styles
        self.colors = {
            'bg': '#307DF6',
            'button_bg': '#ffffff',
            'button_fg': '#307DF6',
            'text': '#ffffff',
            'grid_lines': '#e0e0e0'
        }

        self.root.configure(bg=self.colors['bg'])
        self.init_welcome_screen()

    def create_styled_button(self, text, command, is_secondary=False):
        button = RoundedButton(
            self.root,
            text=text,
            command=command,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg']
        )
        button.pack(pady=5)
        return button

    def init_welcome_screen(self):
        self.clear_screen()

        tk.Frame(self.root, height=50, bg=self.colors['bg']).pack()

        title = tk.Label(
            self.root,
            text="Sudoku",
            font=("Arial", 36, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title.pack(pady=(20, 40))

        self.create_styled_button("PLAY", self.init_play_mode)
        self.create_styled_button("CUSTOM BOARD", self.init_custom_board)

    def init_custom_board(self):
        self.clear_screen()

        tk.Label(
            self.root,
            text="Custom Board",
            font=("Arial", 24),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=(40, 30))

        size_label = tk.Label(
            self.root,
            text="Enter Board Size (e.g., 4, 9, 16):",
            font=("Arial", 16),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        size_label.pack(pady=10)

        self.size_entry = tk.Entry(self.root, font=("Arial", 16), justify="center", width=10)
        self.size_entry.pack(pady=10)

        self.create_styled_button("GENERATE BOARD", self.generate_custom_board)
        self.create_styled_button("BACK", self.init_welcome_screen, is_secondary=True)

    def generate_custom_board(self):
        try:
            size = int(self.size_entry.get())
            if size in [4, 9, 16]:  # Valid Sudoku sizes
                self.start_custom_board(size)
            else:
                raise ValueError("Invalid size")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid board size (4, 9, 16).")

    def start_custom_board(self, size):
        self.clear_screen()

        board_container = tk.Frame(
            self.root,
            bg='white',
            highlightbackground='#ffffff',
            highlightthickness=1,
            bd=0
        )
        board_container.pack(padx=20, pady=20)

        self.entries = []
        for i in range(size):
            row_entries = []
            for j in range(size):
                cell_frame = tk.Frame(
                    board_container,
                    borderwidth=1,
                    relief="solid",
                    bg=self.colors['grid_lines']
                )
                cell_frame.grid(row=i, column=j, padx=0, pady=0)

                entry = tk.Entry(
                    cell_frame,
                    width=2,
                    font=("Arial", 20),
                    justify="center",
                    relief="flat",
                    fg='#307DF6',
                    bg='white'
                )
                entry.pack(padx=8, pady=8)

                row_entries.append(entry)
            self.entries.append(row_entries)

        self.create_styled_button("BACK", self.init_custom_board, is_secondary=True)

    def init_play_mode(self):
        self.clear_screen()

        tk.Label(
            self.root,
            text="Select Difficulty",
            font=("Arial", 24),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=(40, 30))

        self.create_styled_button("EASY", lambda: self.start_game("easy"))
        self.create_styled_button("MEDIUM", lambda: self.start_game("medium"))
        self.create_styled_button("HARD", lambda: self.start_game("hard"))

        self.create_styled_button("BACK", self.init_welcome_screen, is_secondary=True)

    def start_game(self, difficulty):
        self.clear_screen()
        self.current_board = self.player_mode.generate_puzzle(difficulty)

        if difficulty == "medium":
            self.player_mode.checks_left = 15
        elif difficulty == "hard":
            self.player_mode.checks_left = 10
        else:
            self.player_mode.checks_left = -1  # Unlimited for easy

        header_frame = tk.Frame(self.root, bg=self.colors['bg'])
        header_frame.pack(pady=(20, 10))

        tk.Label(
            header_frame,
            text=f"{difficulty.upper()}",
            font=("Arial", 18),
            bg=self.colors['bg'],
            fg='white'
        ).pack()

        # Update the score label
        self.score_label = tk.Label(
            self.root,
            text=f"Score: {self.player_mode.score}",
            font=("Arial", 16),
            bg=self.colors['bg'],
            fg='white'
        )
        self.score_label.pack(pady=(10, 20))

        board_container = tk.Frame(
            self.root,
            bg='white',
            highlightbackground='#ffffff',
            highlightthickness=1,
            bd=0
        )
        board_container.pack(padx=20, pady=20)

        self.entries = []
        for i in range(9):
            row_entries = []
            for j in range(9):
                border_size = 1
                if i % 3 == 0 and i != 0:
                    border_size = 2
                if j % 3 == 0 and j != 0:
                    border_size = 2

                cell_frame = tk.Frame(
                    board_container,
                    borderwidth=border_size,
                    relief="solid" if border_size > 1 else "groove",
                    bg=self.colors['grid_lines']
                )
                cell_frame.grid(row=i, column=j, padx=0, pady=0)

                value = self.current_board[i][j]
                entry = tk.Entry(
                    cell_frame,
                    width=2,
                    font=("Arial", 20),
                    justify="center",
                    relief="flat",
                    fg='#307DF6',
                    bg='white'
                )
                entry.pack(padx=8, pady=8)

                if value != 0:
                    entry.insert(0, str(value))
                    entry.config(state="disabled", disabledbackground="white")
                row_entries.append(entry)
            self.entries.append(row_entries)

        button_frame = tk.Frame(self.root, bg=self.colors['bg'])
        button_frame.pack(pady=20)

        check_button = RoundedButton(
            button_frame,
            "CHECK",
            self.check_move,
            width=100,
            height=35,
            corner_radius=17,
            bg='#ffffff',
            fg='#307DF6'
        )
        check_button.pack(side=tk.LEFT, padx=10)

        self.hint_button = RoundedButton(
            button_frame,
            f"HINT ({self.player_mode.hint_system.hints_left})",
            self.use_hint,
            width=100,
            height=35,
            corner_radius=17,
            bg='#ffffff',
            fg='#307DF6'
        )
        self.hint_button.pack(side=tk.LEFT, padx=10)

        complete_button = RoundedButton(
            button_frame,
            "COMPLETE",
            self.complete_game,
            width=100,
            height=35,
            corner_radius=17,
            bg='#ffffff',
            fg='#307DF6'
        )
        complete_button.pack(side=tk.LEFT, padx=10)

        solve_button = RoundedButton(
            button_frame,
            "SOLVE",
            self.solve_current_board,
            width=100,
            height=35,
            corner_radius=17,
            bg='#ffffff',
            fg='#307DF6'
        )
        solve_button.pack(side=tk.LEFT, padx=10)

        self.create_styled_button("BACK", self.init_welcome_screen, is_secondary=True)

    def check_move(self):
        if self.player_mode.checks_left == 0:
            messagebox.showinfo("Check Limit Reached", "You have used all your checks!")
            return

        if self.player_mode.checks_left > 0:
            self.player_mode.checks_left -= 1

        for i in range(9):
            for j in range(9):
                cell = self.entries[i][j]
                if cell.get().isdigit():
                    value = int(cell.get())
                    if self.player_mode.check_move(i, j, value):
                        cell.config(bg="#e8f5e9")
                    else:
                        cell.config(bg="#ffebee")
                else:
                    cell.config(bg="white")

        if self.player_mode.checks_left > 0:
            messagebox.showinfo("Checks Remaining", f"{self.player_mode.checks_left} checks remaining.")

    def solve_current_board(self):
        board = [[int(entry.get()) if entry.get().isdigit() else 0 for entry in row] for row in self.entries]
        solution = solve_sudoku(board)
        if solution:
            self.update_board(solution)
        else:
            messagebox.showerror("Error", "No solution exists for this board.")

    def complete_game(self):
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                if value.isdigit():
                    self.player_mode.current_board[i][j] = int(value)
                else:
                    self.player_mode.current_board[i][j] = 0

        if self.player_mode.is_game_complete():
            self.player_mode.update_score_for_complete()
            self.score_label.config(text=f"Score: {self.player_mode.score}")
            messagebox.showinfo("Congratulations!", f"You completed the game!\nYour score: {self.player_mode.score}")
        else:
            messagebox.showwarning("Not Complete", "The board is not yet completed correctly.")

    def use_hint(self):
        hint = self.player_mode.use_hint()
        if hint:
            row, col, value = hint
            self.entries[row][col].insert(0, str(value))
            self.entries[row][col].config(state="disabled", disabledbackground="#e8f5e9")
            self.player_mode.update_score_for_hint()
            self.score_label.config(text=f"Score: {self.player_mode.score}")
            self.hint_button.itemconfig(self.hint_button.text, text=f"HINT ({self.player_mode.hint_system.hints_left})")
        else:
            messagebox.showinfo("No Hints", "No hints available!")

    def update_board(self, solution):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(solution[i][j]))
                self.entries[i][j].config(state="disabled", disabledbackground="#f5f5f5")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ModernSudokuApp()
    app.run()