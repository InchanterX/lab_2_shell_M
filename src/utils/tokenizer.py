from src.utils.constants import MASTER_RE
from typing import Any
from dataclasses import dataclass


@dataclass
class Command_Token:
    type: str
    value: Any
    pos: int


class Tokenizer:

    def __init__(self) -> None:
        pass

    def tokenize(self, command: str) -> list[Command_Token]:
        tokens: list[Command_Token] = []
        order = 0
        for element in MASTER_RE.finditer(command):
            kind = element.lastgroup
            content = element.group()
            position = order
            if kind == "SPACE":
                pass
            elif kind == "UNKNOWN":
                raise SyntaxError(
                    f"Невалидное значение {content!r} на позиции {order}!"
                )
            else:
                tokens.append(Command_Token(kind, content, position))
                order += 1
        return tokens
