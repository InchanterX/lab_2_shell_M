import os


class Ls:
    '''
    Command "list"
    '''

    def __init__(self) -> None:
        self.result

    def ls(self, long_flag: list[str], parameters: list[str]) -> str:
        if parameters == []:
            parameters.append["."]


COMMAND_INFO = {
    "name": "ls",
    "function": Ls,
    "entry-point": "ls",
    "flags": ["all", "long", "human-readable", "help"],
    "aliases": {"a": "all", "l": "long", "h": "human-readable"},
    "description": "List files in the given folder."
}
