import src.utils.constants as constants
from typing import Any
from dataclasses import dataclass
import logging


@dataclass
class Command_Token:
    '''
    Creates dataclass for tokens.
    Consists of 3 positions. One for token type, one token's value
    and one for it's original position in the given command
    '''
    type: str
    value: Any
    pos: int


class Tokenizer:
    '''
    Group the result of regular expression work to the list of elements,
    that builds according to the dataclass.
    Process it elements by excluding spaces and checking for unexpected values
    '''

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def tokenize(self, command: str) -> list[Command_Token]:
        tokens: list[Command_Token] = []
        order = 0
        last_element = None

        for element in constants.MASTER_RE.finditer(command):
            # separate element parameters for a simpler usage
            kind = element.lastgroup
            content = element.group()
            position = order

            # exclude spaces b/c they are insignificant
            if kind == "SPACE":
                last_element = kind
            # raise a error if meets an unknown token
            elif kind == "UNKNOWN":
                self._logger.error(
                    f"Invalid value {content} was placed on the position {order}.")
                raise SyntaxError(
                    f"Invalid value {content} on position {order}!"
                )
            # unite the parameters parts if they were given partially in quotes
            elif tokens and last_element and last_element != "SPACE" and tokens[-1].type in ["UNQUOTED_PARAMETER", "QUOTED_PARAMETER"] and kind in ["UNQUOTED_PARAMETER", "QUOTED_PARAMETER"]:
                tokens[-1].value += content
                tokens[-1].type = "QUOTED_PARAMETER"
            # in all other cases just adds token to the list
            else:
                # check if kind is None
                if kind is None:
                    self._logger.error(
                        f"Unexpected None in the token type for {content}.")
                    raise SyntaxError(
                        f"Unexpected None in the token type for {content}.")
                tokens.append(Command_Token(kind, content, position))
                order += 1
            last_element = kind

        self._logger.debug(f"Converted user\'s input command into {tokens}.")
        return tokens
