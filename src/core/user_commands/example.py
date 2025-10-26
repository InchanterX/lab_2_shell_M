# import src.utils.constants


class Example:
    '''
    Command "list"
    '''

    def __init__(self) -> None:
        pass

    def example(self) -> None:
        pass


COMMAND_INFO = {
    "name": "example",
    "function": Example,
    "entry-point": "example",
    "flags": ["long", "all"],
    "aliases": {},
    "description": "Do nothing."
}
