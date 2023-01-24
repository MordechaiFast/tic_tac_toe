from dataclasses import dataclass
from functools import cache, cached_property
from random import choice, random
import re
import textwrap
import time
from typing import Any, List, Tuple

class GameState:
    """Parent class for the current state of many possible games"""

    @property
    def won(self) -> bool:
        ...
    
    win_on_my_turn = False

    def move(self, var) -> 'GameState':
        """Performs a move, if valid, and returns the game's state as 
        a new instance"""
        ...

    @property
    def possible_moves(self) -> List[Tuple[Any, "GameState"]]:
        """Returns a discription of the move and the new GameState 
        for each of the possible moves"""
        ...

    @property
    def tie(self) -> bool:
        if self.won:
            return False
        elif [*self.possible_moves] == []:
            return True
        else:
            return False


TicTacToe_WINNING_COMBOS = (
    [[(row, n) for n in (0, 1, 2)] for row in (0, 1, 2)] +
    [[(n, col) for n in (0, 1, 2)] for col in (0, 1, 2)] +
    [[(n, n  ) for n in (0, 1, 2)]] +
    [[(n, 2-n) for n in (0, 1, 2)]]
)

@dataclass(frozen=True)
class TicTacToeGrid(GameState):
    matrix: str = ' ' * 9
    
    def move(self, position: Tuple[int,int], mark: str) -> 'TicTacToeGrid':
        row, col = position
        index = row * 3 + col
        if self.matrix[index] == ' ':
            new_matrix = self.matrix[:index] + mark + self.matrix[index + 1:]
            return TicTacToeGrid(new_matrix)
        else:
            raise ValueError('Invalid move')

    @cached_property
    def won(self) -> bool:
        for combo in TicTacToe_WINNING_COMBOS:
            if (self.matrix[combo[0][0] * 3 + combo[0][1]]
             == self.matrix[combo[1][0] * 3 + combo[1][1]]
             == self.matrix[combo[2][0] * 3 + combo[2][1]]
             != ' '):
                return True
        return False

    @property
    def potential_moves(self):
        return [(row, col) for row in range(3) for col in range(3)]

    @cached_property
    def possible_moves(self) -> List[Tuple[Any, GameState]]:
        x_count = self.matrix.count('X')
        o_count = self.matrix.count('O')
        next_mark = ('X' if x_count == o_count else 'O')
        moves = []
        for position in self.potential_moves:
            try:
                moves.append((position, self.move(position, next_mark)))
            except ValueError:
                continue
        return moves

def print_grid(grid: TicTacToeGrid) -> None:
    print('\033c', end='')
    print(
        textwrap.dedent(
            """\
             A   B   C
           ------------
        1 ┆  {0} │ {1} │ {2}
          ┆ ───┼───┼───
        2 ┆  {3} │ {4} │ {5}
          ┆ ───┼───┼───
        3 ┆  {6} │ {7} │ {8}
        """
        ).format(*grid.matrix)
    )

def grid_input(prompt: str) -> Tuple[int, int]:
    while True:
        entry = input(prompt).strip()
        if re.match('[abcABC][123]', entry):
            col, row = entry
            break
        elif re.match('[123][abcABC]', entry):
            row, col = entry
            break
        else:
            print('Specify your move in the form of A1 or 1A')
    row = int(row) - 1
    col = ord(col.upper()) - ord('A')
    return row, col

def play_tictactoe():
    grid = TicTacToeGrid()
    print_grid(grid)

    while not grid.won and not grid.tie:
        #X's turn - the Human
        """ try:
            grid = grid.move(grid_input('Your turn, X: '), 'X')
        except ValueError:
            print('Invalid move')
            continue """
        #x's turn - the dumb computer
        time.sleep(.25)
        grid = grid.move(bad_move(grid), 'X')
        #Between odd numbered turns
        print_grid(grid)
        if grid.won:
            print('X wins')
        elif grid.tie:
            print('Tie game')
        else:
            #O's turn - the computer
            time.sleep(.25)
            grid = grid.move(good_move(grid), 'O')
            #Between even numbered turns
            print_grid(grid)
            if grid.won:
                print('O wins')

@cache
def minimax(game: GameState, my_turn: bool) -> int:
    if game.won:
        if game.win_on_my_turn:
            return 1 if my_turn else -1
        else:
            return 1 if not my_turn else -1
    elif game.tie:
        return 0
    else:
        return (max if my_turn else min)(
            minimax(next_state, not my_turn)
            for move, next_state in game.possible_moves
        )

def good_move(game: GameState):
    move_index = [
        (move, minimax(next_state, my_turn=False))
        for move, next_state in game.possible_moves
    ]
    best_option_score = max(score for move, score in move_index)
    good_moves = [
        move
        for move, score in move_index
        if score == best_option_score
    ]
    return choice(good_moves)

def bad_move(game: GameState):
    return choice([move for move, state in game.possible_moves])
    
if __name__ == '__main__':
    play_tictactoe()