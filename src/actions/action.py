"""Adventure Game 1: The file exporting Action, which manages puzzles and custom instructions.

Note that due to cyclic imports, we had to import the entire model for type hints.
"""
from __future__ import annotations

import src.actions


class Action:
    """An action, once executed, modifies the state of the world/player or presents
    the player new information. This class is responsible for running multiple instructions
    together, making sure instructions are executed with respect to their execution types.

    Instance Attributes:
    - name: The name of the action, which is what the player will type into the console.
    - instructions: The list of instructions the action is composed of.
    """
    name: str
    instructions: list[src.actions.instruction.Instruction]

    def __init__(self, name: str, instructions: list[src.actions.instruction.Instruction]) -> None:
        """Create an Action.
        """
        self.name = name
        self.instructions = instructions

    def execute(self, context: src.actions.context.Context, shallow: bool) -> bool:
        """Execute the action with the given arguments, returning whether the execution succeeded.
        Shallow executions are run every time an action is available to the user. They help alert the
        user with their options, such as the description of the action.
        """
        raise NotImplementedError

    def _execute_given(
            self,
            execution_condition: src.actions.excondition.ExecutionCondition,
            context: src.actions.context.Context
    ) -> bool:
        """Executes instructions given the execution condition, returning whether they succeeded.
        """
        i = 0
        while i < len(self.instructions):
            instruction = self.instructions[i]
            if instruction.execution_condition == execution_condition:
                success = instruction.unchecked_execute(context)
                if not success:
                    SingleAction._execute_while_fail(
                        self.instructions[i + 1:], context
                    )
                    return False
            i += 1
        return True

    @staticmethod
    def _execute_while_fail(
            instructions: list[src.actions.instruction.Instruction],
            context: src.actions.context.Context
    ) -> None:
        """Execute all instructions with # execution type sequentially, until all # instructions are done.
        """
        if len(instructions) == 0:
            return

        i = 0
        # while <there are instructions> and <instruction is fail>
        while i < len(instructions) \
                and instructions[i].execution_condition == src.actions.excondition.ExecutionCondition.FAIL:
            instructions[i].unchecked_execute(context)
            i += 1

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class BackgroundAction(Action):
    """This class inherits Action, allowing the action to run in the background. These types of
    actions execute whenever user changes a location, and they execute each single time."""

    def __init__(self, name: str, instructions: list[src.actions.instruction.Instruction]) -> None:
        """Initialize a BackgroundAction
        """
        super().__init__(name, instructions)

    def execute(self, context: src.actions.context.Context, _shallow: bool) -> bool:
        # In this context, whether it is shallow or not does not matter, since
        # this is a background action. The player does not have to be alerted
        # of this.
        return self._execute_given(
            execution_condition=src.actions.excondition.ExecutionCondition.ONCE,
            context=context
        )


class SingleAction(Action):
    """This class inherits Action, however it can only be executed once, except for
    shallow executions.

    Instance Attributes:
        - action_location_id: The location (ID) of the action.
        - completed: Whether the action has successfully run before.
    """
    action_location_id: int
    completed: bool

    def __init__(
            self,
            name: str,
            action_location_id: int,
            instructions: list[src.actions.instruction.Instruction]
    ) -> None:
        """Initialize an Action.
        """
        super().__init__(name, instructions)
        self.action_location_id = action_location_id
        self.completed = False

    def execute(self, context: src.actions.context.Context, shallow: bool) -> bool:
        """Execute the action with the given arguments, returning whether the execution succeeded.
        Shallow executions are run every time an action is available to the user. They help alert the
        user with their options, such as the description of the action.
        """
        # If it's a shallow execute but the action is completed already, skip.
        # If it's a shallow execute but the action is not completed, execute the `-` calls.
        if shallow and not self.completed:
            return self._execute_given(
                execution_condition=src.actions.excondition.ExecutionCondition.ACTION_NOT_COMPLETED,
                context=context
            )
        elif not shallow and self.completed:
            return self._execute_given(
                execution_condition=src.actions.excondition.ExecutionCondition.ACTION_COMPLETED,
                context=context
            )
        # We cannot refactor to else statement, since we would have to create another
        # case where `if shallow_execute and self.completed`, but we want to ignore that
        # case.
        elif not shallow and not self.completed:  # ONCE
            success = self._execute_given(
                execution_condition=src.actions.excondition.ExecutionCondition.ONCE,
                context=context
            )

            if success:
                self.completed = True
            return success
        else:
            return True

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        # Since the name of the action must be unique in the same locations.
        return f"{self.name.lower()}:{self.action_location_id}"


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ["src.actions"]
    })
