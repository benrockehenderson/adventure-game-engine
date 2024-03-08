"""Adventure Game 1: A parser for ActionScript

Here, we have avoided to build a full lexer. Although we have started by implementing
a lexer first, we have simplified ActionScript using execution types ($, #, +, -), which
has allowed us to build a simple parser directly and skip the lexing process.
"""
from __future__ import annotations
from src.actions.excondition import ExecutionCondition
from src.actions.instruction import Instruction


class ActionScriptParser:
    """A class representing the ActionScript Parser.

    Instance Attributes:
        - lines: The list of functions being called.
    """
    lines: list[str]

    def __init__(self, lines: list[str]) -> None:
        """Initialize a parser.
        """
        self.lines = lines

    def compile(self) -> list[Instruction]:
        """Compile and return a list of instructions.
        """
        instructions = []
        for line in self.lines:
            line = line.strip()
            if line != '':
                execution_condition_chr = line[0]
                execution_condition = ExecutionCondition.from_str(execution_condition_chr)

                operation, arguments = ActionScriptParser._parse_instruction(line[1:])
                instructions.append(Instruction(
                    operation=operation, execution_condition=execution_condition, arguments=arguments
                ))
        return instructions

    @staticmethod
    def _parse_instruction(line: str) -> tuple[str, list[str | int]]:
        args_start_inclusive = line.find('(') + 1
        operation = line[:args_start_inclusive - 1]
        args_end_exclusive = line.rfind(')')

        args = []
        current_arg = ''
        in_quotes = False
        for char in line[args_start_inclusive:args_end_exclusive]:
            # escaped quote
            # If <character is empty> and (<we haven't parsed anything yet> OR <last parsed is not escape character>)
            if char == '"' and (len(current_arg) == 0 or current_arg[-1] != '\\'):
                in_quotes = not in_quotes
                current_arg += char
            elif char == ',' and not in_quotes:
                args.append(current_arg.strip())
                current_arg = ''
            else:
                current_arg += char

        if current_arg != '':
            args.append(current_arg.strip())

        for i, arg in enumerate(args):
            if arg[0] == '"' and arg[-1] == '"':
                # This is a string, unescape quotes
                args[i] = arg[1:-1].replace('\\"', '"')
            else:
                # This argument is an integer
                args[i] = int(arg)

        return operation, args


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['src.actions.instruction', 'src.actions.excondition'],
    })
