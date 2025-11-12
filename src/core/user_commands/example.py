

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
    "function": lambda: Example(),
    "entry-point": "example",
    "flags": ["help"],
    "aliases": {},
    "description": "Do nothing."
}
