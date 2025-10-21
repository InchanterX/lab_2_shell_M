# import src.utils.constants


class ls:
    '''
    Command "list"
    '''

    def __init__(self) -> None:
        pass

    def ls(self) -> None:
        pass


COMMAND_INFO = {
    "name": "ls",
    "flags": ["-l"],
    "description": "List files in the given folder.",
    "function": ls
}
