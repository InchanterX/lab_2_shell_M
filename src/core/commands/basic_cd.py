import src.utils.constants as constants
import os


class Cd:
    '''
    Command "cd"
    '''

    def __init__(self) -> None:
        pass

    def cd(self, long_flag: list[str], parameters: list[str]) -> str:
        if long_flag != [] and long_flag[0] == "help":
            return "cd"  # should return values from separate module "help" that forms the message depends on the command
        if parameters == []:
            constants.CURRENT_DIR = constants.USER_HOME_DIR

        for parameter in parameters:
            if parameter[0] == "~":
                parameter = constants.USER_HOME_DIR + parameter[1:]
                if os.path.isfile(parameter):
                    raise SyntaxError("You can't switch to a file!")
                elif os.path.isdir(parameter):
                    constants.CURRENT_DIR = parameter
                else:
                    raise SyntaxError(f"Path {parameter} is invalid!")
            if parameter[0:2] == "..":
                if constants.CURRENT_DIR == "/":
                    raise SyntaxError("You can't switch any higher!")
                current_dir_copy = constants.CURRENT_DIR
                while current_dir_copy[-1] != "/":
                    current_dir_copy[:-1]
                current_dir_copy[:-1]
                if os.path.isdir(current_dir_copy+parameter[2:]):
                    constants.CURRENT_DIR = current_dir_copy + \
                        parameter[2:]
                else:
                    raise SyntaxError(
                        f"Path {constants.CURRENT_DIR_copy+parameter[2:]} is invalid!")
            elif parameter[0] == ".":
                if os.path.isdir(constants.CURRENT_DIR+parameter[1:]):
                    constants.CURRENT_DIR += parameter[1:]
                else:
                    raise SyntaxError(
                        f"Path {constants.CURRENT_DIR+parameter[1:]} is invalid!"
                    )
            elif parameter[0] == "/":
                if os.path.isdir(parameter):
                    constants.CURRENT_DIR = parameter
                else:
                    raise SyntaxError(f"Path {parameter} is invalid!")
            else:
                if os.path.isdir(constants.CURRENT_DIR + "/" + parameter):
                    constants.CURRENT_DIR = constants.CURRENT_DIR + "/" + parameter
                else:
                    raise SyntaxError(f"Path {parameter} is invalid!")


COMMAND_INFO = {
    "name": "cd",
    "function": Cd,
    "entry-point": "cd",
    "flags": ["help"],
    "aliases": {},
    "description": "Give an ability to switch between folders."
}
