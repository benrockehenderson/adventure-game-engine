"""Adventure Game 1: Common enum definition import used for ActionScript functions.
"""
from __future__ import annotations
from enum import Enum, auto

from src.errors import UnknownExecutionCondition


class ExecutionCondition(Enum):
    """Enum describing the possible execution types of a function in ActionScript.
    """
    ACTION_NOT_COMPLETED = auto()
    ACTION_COMPLETED = auto()
    ONCE = auto()
    FAIL = auto()

    @staticmethod
    def from_str(character: str) -> ExecutionCondition:
        """Convert a given character to the ExecutionCondition enum.
        """
        match character:
            case '-':
                return ExecutionCondition.ACTION_NOT_COMPLETED
            case '+':
                return ExecutionCondition.ACTION_COMPLETED
            case '$':
                return ExecutionCondition.ONCE
            case '#':
                return ExecutionCondition.FAIL
        raise UnknownExecutionCondition(f"Unknown execution condition: {character}")

    def __str__(self) -> str:
        match self:
            case ExecutionCondition.ACTION_NOT_COMPLETED:
                return '-'
            case ExecutionCondition.ACTION_COMPLETED:
                return '+'
            case ExecutionCondition.ONCE:
                return '$'
            case ExecutionCondition.FAIL:
                return '#'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['src.errors', 'enum']
    })
