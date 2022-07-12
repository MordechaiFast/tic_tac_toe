"""A tic-tac-toe game built wiht Python and Tkinter"""

from itertools import cycle
import tkinter as tk
from tkinter.font import Font
from typing import NamedTuple, Tuple

class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = None

DEFAULT_PLAYERS = (Player('X', 'blue'), Player('O', 'green'))
BOARD_SIZE = 3

class Game:
    def __init__(self,
        players: Tuple[Player, Player] = DEFAULT_PLAYERS,
        board_size: int = BOARD_SIZE
    ) -> None:
        self._turn_generator = cycle(players)
        self._moves_matrix = [
            [Move(row, col) for col in range(board_size)]
            for row in range(board_size)
        ]
        self.board_size = board_size
        self._winning_combos = self._get_winning_combos()
        self.toggle_player()

    def _get_winning_combos(self) -> list:
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._moves_matrix
        ]
        cols = [list(col) for col in zip(*rows)]
        row_diagonal = [row[i] for i, row in enumerate(rows)]
        col_diagonal = [col[j] for j, col in enumerate(reversed(cols))]
        return rows + cols + [row_diagonal, col_diagonal]

    def validate(self, move: Move) -> bool:
        if self.win():
            return False
        if self._moves_matrix[move.row][move.col].label is None:
            return True
        else:
            return False

    def record(self, move: Move) -> None:
        self._moves_matrix[move.row][move.col] = move

    def win(self) -> bool:
        """Returns True is there is a winning combonation, 
        otherwise returns False"""
        for combo in self._winning_combos:
            in_combo = {
                self._moves_matrix[row][col].label
                for row, col in combo
            }
            if len(in_combo) == 1 and None not in in_combo:
                self.winner_combo = combo
                return True
        return False

    def tie(self) -> bool:
        """Returns True if all winning combonations have been blocked,
        otherwise returns False"""
        blocked_combo = []
        for combo in self._winning_combos:
            if len({
                self._moves_matrix[row][col].label
                for row, col in combo
                if self._moves_matrix[row][col].label is not None
            }) == 2:
                blocked_combo.append(True)
            else:
                blocked_combo.append(False)
        return all(blocked_combo)

    def toggle_player(self) -> None:
        self.current_player = next(self._turn_generator)

class Board(tk.Tk):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self.title('Tic-Tac-Toe Game')
        self.game = game
        self._cells = {}
        self._create_board_display(text='Ready?')
        self._create_board_grid()

    def play_move(self, clicked_btn: tk.Event):
        """Handle a player's move"""
        row, col = self._cells[clicked_btn.widget]
        move = Move(row, col, self.game.current_player.label)
        if self.game.validate(move):
            self.game.record(move)
            self._update_button(clicked_btn.widget, self.game.current_player)
            if self.game.win():
                self._highlight_cells(self.game.winner_combo)
                self._update_display(
                    msg=f'{self.game.current_player.label} wins!',
                    color=self.game.current_player.color
                )
            elif self.game.tie():
                self._update_display(msg='Cats game', color='red')
            else:
                self.game.toggle_player()
                self._update_display(
                    msg=f"{self.game.current_player.label}'s turn",
                    color=self.game.current_player.color
                )

    def _create_board_display(self, text: str):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text=text,
            font=Font(size=28, weight='bold')
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self.game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self.game.board_size):
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
                button.bind('<ButtonPress-1>', self.play_move)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky='nesw'
                )

    def _update_button(self, clicked_button: tk.Button, player: Player):
        clicked_button.config(text=player.label)
        clicked_button.config(fg=player.color)

    def _update_display(self, msg: str, color='black'):
        self.display['text'] = msg
        self.display['fg'] = color

    def _highlight_cells(self, cells: list):
        pass

if __name__ == '__main__':
    tic_tac_toe = Game()
    Board(tic_tac_toe).mainloop()