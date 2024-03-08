"""Adventure Game 1: Common enum definition to describe the directions.
"""

from __future__ import annotations
from enum import Enum, auto

from src.errors import InvalidDirection


class Direction(Enum):
    """Enum representing the directions east, west, north, and south.
    """
    EAST = auto()
    WEST = auto()
    NORTH = auto()
    SOUTH = auto()

    def __str__(self) -> str:
        match self:
            case Direction.NORTH:
                return "north"
            case Direction.EAST:
                return "east"
            case Direction.SOUTH:
                return "south"
            case Direction.WEST:
                return "west"

    def offset(self) -> tuple[int, int]:
        """Return the R^2 vector direction of the enum.

        For example, any movement in the north direction represents a negative change
        in the y coordinate, whereas south represents a positive change. Similarly,
        moving towards east increases the x value, and moving towards west represents a
        negative change in the x value.
        """
        match self:
            case Direction.NORTH:
                return 0, -1
            case Direction.EAST:
                return 1, 0
            case Direction.SOUTH:
                return 0, 1
            case Direction.WEST:
                return -1, 0

    @staticmethod
    def from_str(text: str) -> Direction:
        """Convert a given direction string into the enum representation.
        """
        match text.lower():
            case "north":
                return Direction.NORTH
            case "east":
                return Direction.EAST
            case "south":
                return Direction.SOUTH
            case "west":
                return Direction.WEST
        raise InvalidDirection(f"Invalid direction: {text}")


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['src.errors', 'enum'],
    })
