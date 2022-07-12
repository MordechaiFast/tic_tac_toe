"""A tic-tac-toe game built wiht Python and Tkinter"""

from itertools import cycle
import tkinter as tk
from tkinter.font import Font
from typing import NamedTuple

class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = None

BOARD_SIZE = 3
DEFAULT_PLAYERS = (Player('X', 'blue'), Player('O', 'green'))

class Board(tk.Tk):
    def __init__(self, board_size=BOARD_SIZE) -> None:
        super().__init__()
        self.title('Tic-Tac-Toe Game')
        self._cells = {}
        self._create_board_display()
        self._create_board_grid(board_size)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text='Ready?',
            font=Font(size=28, weight='bold')
        )
        self.display.pack()

    def _create_board_grid(self, board_size):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(board_size):
                button = tk.Button(
                    master=grid_frame,
                    text='',
                    font=Font(size=36, weight='bold'),
                    fg='black',
                    width=3,
                    height=2,
                    highlightbackground='lightblue',
                )
                self._cells[button] = (row, col)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky='nesw'
                )

class Game:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE) -> None:
        self.turn_generator = cycle(players)
        self.board_size = board_size
        self.current_player = next(self.turn_generator)
        self._setup_board()
        self._winning_combos = self._get_winning_combos()
        self.winner_combo = []
        self.game_over = False

    def _setup_board(self) -> None:
        self.moves_matrix = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]

    def _get_winning_combos(self) -> list:
        rows = [
            [(move.row, move.col) for move in row]
            for row in self.moves_matrix
        ]
        cols = [list(col) for col in zip(*rows)]
        row_diagonal = [row[i] for i, row in enumerate(rows)]
        col_diagonal = [col[j] for j, col in enumerate(reversed(cols))]
        return rows + cols + [row_diagonal, col_diagonal]

    def validate_move(self, move: Move) -> bool:
        if self.game_over:
            return False
        if self.moves_matrix[move.row][move.col].label is None:
            return True
        else:
            return False

    def record_move(self, move: Move) -> None:
        self.moves_matrix[move.row][move.col] = move

    def check_for_win(self) -> bool:
        for combo in self._winning_combos:
            if len({
                self.moves_matrix[row][col].label
                for row, col in combo
                if self.moves_matrix[row][col] is not None
            }) == 1:
                self.game_over = True
                self.winner_combo = combo
                return True
        return False

    def check_for_tie(self) -> bool:
        blocked_combo = {}
        for combo in self._winning_combos:
            if len({
                self.moves_matrix[row][col].label
                for row, col in combo
                if self.moves_matrix[row][col] is not None
            }) == 2:
                blocked_combo[combo] = True
            else:
                blocked_combo[combo] = False
        return all(blocked_combo)

    def toggle_player(self) -> None:
        self.current_player = next(self.turn_generator)

if __name__ == '__main__':
    Board().mainloop()