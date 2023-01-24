from dataclasses import dataclass
from functools import cache
import random
from time import sleep
from typing import Any, List, Tuple

class GameState:
    """Parent class for the current state of many possible games
    Should be a frozen dataclass for minimax to work quickly."""

    state: Any
    current_player: 'Player'

    @property
    def potential_moves(self) -> List:
        """Returns a list of all moves that might be taken, without 
        validation that the move is legal"""
        ...

    def move(self, var) -> 'GameState':
        """Performs a move, if valid, and returns the game's state as 
        a new instance, with the next player as the current player. 
        Invalid moves raise a ValueError."""
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

    def score(self, player) -> int:
        ...
    
    @property
    def tie(self) -> bool:
        if self.won:
            return False
        elif [*self.possible_moves] == []:
            return True
        else:
            return False

@dataclass(frozen=True)
class Player:
    name: str

    def get_move(self, game: GameState):
        """Returns a discription of the next move to take, as per the 
        player's inteligence, given the current game state"""

    @property
    def opponent(self) -> 'Player':
        player_list = [*reversed(players)]
        for n, player in enumerate(player_list):
            if player is self:
                return player_list[n-1]
        raise ValueError('This player is not in the Players list')
    

@dataclass(frozen=True)
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


def play_engine(game:GameState, player_list: Tuple[Player, Player]):
    """Have players play any turn based game"""

    global players
    players = player_list
    game.display()
    while not game.won and not game.tie:
        player = game.current_player
        try:
            move = player.get_move(game)
            game = game.move(move)
        except ValueError:
            continue
        game.display()
    if game.won:
        scores = [(game.score(player), player) for player in players]
        winner = max(scores)[1]
        print(f"""{winner.name} {'win' if winner.name in ('I', 'You')
            else 'wins'}\n""")
    elif game.tie:
        print('Tie game')


@dataclass(frozen=True)
class SmartComputer(ComputerPlayer):
    
    def inteligent_moves(self, game: GameState) -> List:
        move_index = [
            (move, self.minimax(next_state, my_turn=False))
            for move, next_state in game.possible_moves
        ]
        best_option_score = max(score for move, score in move_index)
        good_moves = [
            move
            for move, score in move_index
            if score == best_option_score
        ]
        return good_moves

    @cache
    def minimax(self, game: GameState, my_turn: bool, best=-1, worst=1) -> int:
        if game.won or game.tie:
            return game.score(self)
        else:
            scores = []
            for move, next_state in game.possible_moves:
                score = self.minimax(next_state, not my_turn, best, worst)
                scores.append(score)
                if my_turn:
                    best = max(best, score)
                else:
                    worst = min(worst, score)
                if worst <= best:
                    break
            return (max if my_turn else min)(scores)

@dataclass(frozen=True)
class DumbComputer(ComputerPlayer):
    def inteligent_moves(self, game: GameState) -> List:
        return [move for move, state in game.possible_moves]