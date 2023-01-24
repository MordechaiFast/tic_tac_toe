from dataclasses import dataclass
from functools import cache
from itertools import cycle
import random
from time import sleep
from typing import Any, Iterable, List, Tuple

class GameState:
    """Parent class for the current state of many possible games
    Should be a frozen dataclass for minimax to work quickly."""

    @property
    def potential_moves(self) -> List:
        """Returns a list of all moves that might be taken, without 
        validation that the move is legal"""
        ...

    def move(self, var) -> 'GameState':
        """Performs a move, if valid, and returns the game's state as 
        a new instance. Invalid moves raise a ValueError."""
        ...

    @property
    def possible_moves(self) -> List[Tuple[Any, "GameState"]]:
        """Returns a discription of the move and the new GameState 
        for each of the possible moves"""
        moves = []
        for move in self.potential_moves:
            try:
                moves.append((move, self.move(move)))
            except ValueError:
                continue
        return moves
    
    def display(self) -> None:
        """Displays the current game state"""

    @property
    def won(self) -> bool:
        ...
    
    win_on_my_turn = False

    @property
    def tie(self) -> bool:
        if self.won:
            return False
        elif [*self.possible_moves] == []:
            return True
        else:
            return False

@dataclass
class Player:
    name: str

    def get_move(self, game: GameState):
        """Returns a discription of the next move to take, as per the 
        player's inteligence, given the current game state"""

@dataclass
class ComputerPlayer(Player):
    name: str = 'I'
    speed: float = 0.0

    def get_move(self, game: GameState):
        move = random.choice(self.inteligent_moves(game))
        sleep(self.speed)
        self.report_move(move)
        return move

    def inteligent_moves(self, game: GameState) -> List:
        ...

    def report_move(self, move) -> None:
        """Reports the move choice made by the computer, if nessecary."""
        pass


def play_engin(game:GameState, players: Iterable):
    """Have players play any turn based game"""

    players = cycle(players)

    game.display()
    player = next(players)

    while not game.won and not game.tie:
        try:
            move = player.get_move(game)
            game = game.move(move)
        except ValueError:
            continue
        game.display()
        player = next(players)
    if game.won:
        if not game.win_on_my_turn:
            player = next(players)
        print(f"""{player.name} {'win' if player.name in ('I', 'You')
            else 'wins'}\n""")
    elif game.tie:
        print('Tie game')


@cache
def minimax(game: GameState, my_turn: bool, best=-1, worst=1) -> int:
    if game.won:
        if game.win_on_my_turn:
            return 1 if my_turn else -1
        else:
            return 1 if not my_turn else -1
    elif game.tie:
        return 0
    else:
        scores = []
        for move, next_state in game.possible_moves:
            score = minimax(next_state, not my_turn, best, worst)
            scores.append(score)
            if my_turn:
                best = max(best, score)
            else:
                worst = min(worst, score)
            if worst <= best:
                break
        return (max if my_turn else min)(scores)

@dataclass
class SmartComputer(ComputerPlayer):
    
    def inteligent_moves(self, game: GameState) -> List:
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
        return good_moves

@dataclass
class DumbComputer(ComputerPlayer):
    def inteligent_moves(self, game: GameState) -> List:
        return [move for move, state in game.possible_moves]
        

@dataclass(frozen=True)
class Pot(GameState):
    """The pot in the game of Nim"""

    count: int

    @property
    def potential_moves(self) -> List:
        return [1, 2, 3]

    def move(self, take: int) -> 'Pot':
        if take <= self.count:
            return Pot(self.count - take)
        else:
            raise ValueError

    @property
    def won(self):
        return self.count == 0

    win_on_my_turn = True

    def display(self) -> None:
        print(f"The pot now has {self.count} tokens")

@dataclass
class HumanNim(Player):
    name: str = 'You'

    def get_move(self, pot: Pot):
        address = 'Your' if self.name == 'You' else f"{self.name}'s"
        take = int(input(f"{address} turn. Take 1, 2, or 3 tokens: "))
        if take in pot.potential_moves:
            return take
        else:
            raise ValueError

@dataclass
class ComputerNimSmart(SmartComputer):
    def report_move(self, move) -> None:
        print(f"{self.name} take{'' if self.name == 'I' else 's'} {move}.",
         end=' ')

@dataclass
class ComputerNimDumb(DumbComputer):
    def report_move(self, move) -> None:
        print(f"{self.name} {'take' if self.name == 'I' else 'takes'} {move}.",
         end=' ')


if __name__ == '__main__':
    for n in range(13, 11, -1):
        play_engin(Pot(n), [ComputerNimSmart('A'), ComputerNimDumb('B')])
    #play_engin(Pot(int(10 * random()) + 10), [HumanNim(), ComputerNimSmart()])