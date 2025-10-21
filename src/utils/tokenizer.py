from typing import Any
# import src.utils.constants


class Command_Token:
    type: str
    value: Any


class Tokenizer:

    def __init__(self) -> None:
        pass

    def tokenize(self, command: str) -> list[Command_Token]:
        command = r"ls \d\repository\ -l"

        tokens = command.split(" ")
        print(tokens)
