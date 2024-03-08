"""Adventure Game 1: The common Instruction export, the smallest unit of execution.
"""
from __future__ import annotations
from dataclasses import dataclass

from src.direction import Direction
from src.actions.excondition import ExecutionCondition
import src.actions


@dataclass
class Instruction:
    """The smallest unit of execution in ActionScript actions.

    Instance Attributes:
        - operation: A valid operation string caught by any branch in the `unchecked_execute` method.
        - execution_condition: A valid execution condition.
        - arguments: The list of arguments passed to the operation.
    """
    operation: str
    execution_condition: ExecutionCondition
    arguments: list[str | int]

    def unchecked_execute(self, context: src.actions.context.Context) -> bool:
        """Execute the instruction without checking the execution condition, returning whether it has succeeded.

        Any instruction cannot be executed with respects to its execution condition, given that each instruction would
        require a broader context, including the result of the previous instruction.

        Therefore, the bulk execution of instructions with respect to operations are handled in the Action class.
        """
        match self.operation:
            # print("...")
            case 'print':
                print(*self.arguments)
                return True

            # add_points(10)
            case 'add_points':
                context.player.points += self.arguments[0]
                return True

            # take_points(10)
            case 'take_points':
                context.player.points = max(0, context.player.points - self.arguments[0])
                return True

            # has_item("T-Card")
            case 'has_item':
                return any(self.arguments[0].lower() == repr(inv_item) for inv_item in context.player.inventory)

            # add_item("T-Card")
            case 'add_item':
                if len(self.arguments) == 2:
                    lid = self.arguments[1]
                    location_id = None if lid < 0 else lid
                    context.player.create_add_item(
                        name=self.arguments[0],
                        location_id=location_id
                    )
                else:
                    context.player.create_add_item(
                        name=self.arguments[0],
                        location_id=None
                    )

                return True

            # take_item("T-Card")
            case 'take_item':
                for item in context.player.inventory:
                    if repr(item) == self.arguments[0].lower():
                        context.player.inventory.remove(item)
                        return True
                return False

            # prompt("Bumbly")
            case 'prompt':
                result = input("> ")
                return any(result.lower() == arg.lower() for arg in self.arguments)

            # unlock_direction_at_point(14, "WEST")
            case 'unlock_direction_at_point':
                loc = context.world.locations[self.arguments[0]]
                loc.allowed_movements.add(
                    Direction.from_str(self.arguments[1])
                )
                return True

            # win()
            case 'win':
                context.player.victory = True
                return True

            # steps_less_than(20)
            case 'steps_less_than':
                return context.player.steps < self.arguments[0]

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        """Convert the instruction to a string.

        >>> inst = Instruction('print', ExecutionCondition.ACTION_COMPLETED, ['2^2', '=', 4])
        >>> str(inst)
        '+print("2^2", "=", 4)'
        """
        return f"{self.execution_condition}{self.operation}({', '.join(
            f'"{arg}"' if isinstance(arg, str) else str(arg) for arg in self.arguments
        )})"


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['src.direction', 'src.actions.excondition', 'src.actions'],
        'allowed-io': ['Instruction.unchecked_execute']
    })
