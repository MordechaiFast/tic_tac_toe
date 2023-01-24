from dataclasses import dataclass
import random
from typing import List
from engine import DumbComputer, GameState, Player, SmartComputer, play_engine


@dataclass(frozen=True)
class Pot(GameState):
    """The pot in the game of Nim"""

    count: int
    current_player: Player

    @property
    def potential_moves(self) -> List:
        return [1, 2, 3]

    def move(self, take: int) -> 'Pot':
        if take <= self.count:
            return Pot(self.count - take, self.current_player.opponent)
        else:
            raise ValueError

    @property
    def won(self):
        return self.count == 0

    def score(self, player):
        if self.won:
            if player is self.current_player:
                return 1
            else:
                return -1
        elif self.tie:
            return 0

    def display(self) -> None:
        print(f"The pot now has {self.count} tokens")

@dataclass(frozen=True)
class HumanNim(Player):
    name: str = 'You'

    def get_move(self, pot: Pot):
        address = 'Your' if self.name == 'You' else f"{self.name}'s"
        take = int(input(f"{address} turn. Take 1, 2, or 3 tokens: "))
        if take in pot.potential_moves:
            return take
        else:
            raise ValueError

@dataclass(frozen=True)
class ComputerNimSmart(SmartComputer):
    def report_move(self, move) -> None:
        print(f"{self.name} take{'' if self.name == 'I' else 's'} {move}.",
         end=' ')

@dataclass(frozen=True)
class ComputerNimDumb(DumbComputer):
    def report_move(self, move) -> None:
        print(f"{self.name} {'take' if self.name == 'I' else 'takes'} {move}.",
         end=' ')

if __name__ == '__main__':
    first = HumanNim()
    second = ComputerNimSmart() 
    players = (first, second)
    play_engine(Pot(random.randint(6, 10), first), players)
