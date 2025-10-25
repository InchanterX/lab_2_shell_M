from typing import Any
from dataclasses import dataclass
from src.utils.constants import MASTER_RE
import re


@dataclass
class Command_Token:
    type: str
    value: Any
    pos: int


class Tokenizer:

    def __init__(self) -> None:
        pass

    def tokenize(self, command: str) -> list[Command_Token]:
        tokens = []
        for element in MASTER_RE.finditer(command):
            print(element)
