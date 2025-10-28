import src.utils.constants as constants
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
        last_element = None
        for element in constants.MASTER_RE.finditer(command):
            kind = element.lastgroup
            content = element.group()
            position = order
            if kind == "SPACE":
                last_element = kind
                continue
            elif kind == "UNKNOWN":
                raise SyntaxError(
                    f"Invalid value {content!r} on position {order}!"
                )

            elif tokens and last_element and last_element != "SPACE" and tokens[-1].type in ["UNQUOTED_PARAMETER", "QUOTED_PARAMETER"] and kind in ["UNQUOTED_PARAMETER", "QUOTED_PARAMETER"]:
                tokens[-1].value += content
                tokens[-1].type = "QUOTED_PARAMETER"
            # elif last_element == "QUOTED_PARAMETERS" and (kind == "QUOTED_PARAMETER" or kind == "UNQUOTED_PARAMETER"):
            #     tokens[-1].value += content
            else:
                tokens.append(Command_Token(kind, content, position))
                order += 1
            last_element = kind
        return tokens
