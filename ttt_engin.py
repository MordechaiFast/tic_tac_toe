from dataclasses import dataclass
from functools import cached_property
import re
import textwrap
from typing import List, Tuple
from engine import (GameState, Player,
    play_engine,
    SmartComputer, ComputerPlayer)


TicTacToe_WINNING_COMBOS = (
    [[(row, n) for n in (0, 1, 2)] for row in (0, 1, 2)] +
    [[(n, col) for n in (0, 1, 2)] for col in (0, 1, 2)] +
    [[(n, n  ) for n in (0, 1, 2)]] +
    [[(n, 2-n) for n in (0, 1, 2)]]
)

@dataclass(frozen=True)
class TicTacToeGrid(GameState):
    matrix: str = ' ' * 9
    current_player: Player = None
    
    @property
    def potential_moves(self) -> List:
        return [(row, col) for row in range(3) for col in range(3)]

    def move(self, position: Tuple[int,int]) -> 'TicTacToeGrid':
        row, col = position
        index = row * 3 + col
        if self.matrix[index] == ' ':
            x_count = self.matrix.count('X')
            o_count = self.matrix.count('O')
            mark = ('X' if x_count == o_count else 'O')
            new_matrix = self.matrix[:index] + mark + self.matrix[index + 1:]
            return TicTacToeGrid(new_matrix, self.current_player.opponent)
        else:
            raise ValueError

    @cached_property
    def won(self) -> bool:
        for combo in TicTacToe_WINNING_COMBOS:
            if (self.matrix[combo[0][0] * 3 + combo[0][1]]
             == self.matrix[combo[1][0] * 3 + combo[1][1]]
             == self.matrix[combo[2][0] * 3 + combo[2][1]]
             != ' '):
                return True
        return False

    def score(self, player):
        if self.won:
            if player is not self.current_player:
                return 1 + self.matrix.count(' ')
            else:
                return -(1 + self.matrix.count(' '))
        elif self.tie:
            return 0
            
    
    def display(self) -> None:
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
            ).format(*self.matrix)
        )

@dataclass(frozen=True)
class HumanTTT(Player):

    def get_move(self, grid: TicTacToeGrid) -> Tuple[int, int]:
        entry = input(f'Your turn, {self.name}:').strip()
        if re.match('[abcABC][123]', entry):
            col, row = entry
        elif re.match('[123][abcABC]', entry):
            row, col = entry
        else:
            print('Specify your move in the form of A1 or 1A')
            raise ValueError
        row = int(row) - 1
        col = ord(col.upper()) - ord('A')
        return row, col

    @property
    def opponent(self) -> 'Player':
        player_list = [*reversed(players)]
        for n, player in enumerate(player_list):
            if player is self:
                return player_list[n-1]
        raise ValueError('This player is not in the Players list')

@dataclass(frozen=True)
class PuncuatedComputer(SmartComputer):
    def inteligent_moves(self, game: GameState) -> List:
        move_index = [
            (move, self.minimax(next_state, my_turn=False))
            for move, next_state in game.possible_moves
        ]
        if input() == 'b': breakpoint()
        best_option_score = max(score for move, score in move_index)
        good_moves = [
            move
            for move, score in move_index
            if score == best_option_score
        ]
        return good_moves

    @property
    def opponent(self) -> 'Player':
        player_list = [*reversed(players)]
        for n, player in enumerate(player_list):
            if player is self:
                return player_list[n-1]
        raise ValueError('This player is not in the Players list')

@dataclass(frozen=True)
class DumbComputer(ComputerPlayer):
    def inteligent_moves(self, game: GameState) -> List:
        return [move for move, state in game.possible_moves]

    @property
    def opponent(self) -> 'Player':
        player_list = [*reversed(players)]
        for n, player in enumerate(player_list):
            if player is self:
                return player_list[n-1]
        raise ValueError('This player is not in the Players list')

if __name__ == '__main__':
    players = (DumbComputer('X', speed=.1), PuncuatedComputer('O'))
    play_engine(TicTacToeGrid(current_player=players[0]), players)