"""Adventure Game 1: The Context common export, used to pass data between the game and the instructions.
Due to cyclic imports, we must import src.game_data directly.
"""
from __future__ import annotations
from dataclasses import dataclass
import src.game_data


@dataclass
class Context:
    """Context dataclass is used to minimize the number of function arguments while passing data
    between the game state and the instructions.

    Instance Attributes:
        - world: The game's world state.
        - player: The player of the game.
        - location: The player's current location.
        - global_store: An arbitrary mapping which can be used to pass data between actions.
    """
    world: src.game_data.World
    player: src.game_data.Player
    location: src.game_data.Location


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ["src.game_data"]
    })
