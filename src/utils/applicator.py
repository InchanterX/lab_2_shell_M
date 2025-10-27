from src.utils.tokenizer import Command_Token
from src.utils.constants import REGISTRY


class Applicator:

    def __init__(self, tokens) -> None:

        # list of all command's commands
        self.commands = [
            [command.pos, command.value] for command in tokens if command.type == "COMMAND"]

        # list of all command's flags
        self.short_flags = [
            short_flag.value[1:] for short_flag in tokens if short_flag.type == "SHORT_FLAG"]
        self.long_flags = [
            long_flag.value[2:] for long_flag in tokens if long_flag.type == "LONG_FLAG"
        ]
        self.unique_short_flags = set()
        for short_flag in self.short_flags:
            for char in short_flag:
                self.unique_short_flags.add(char)

        # list of all command's parameters
        self.parameters = [
            parameter.value for parameter in tokens if parameter.type == "UNQUOTED_PARAMETER"
        ] + [
            parameter.value for parameter in tokens if parameter.type == "QUOTED_PARAMETER"
        ]

        self.first_element = tokens[0]
        self.main_command = self.commands[0][1]
        class_name = REGISTRY[self.main_command]["function"]
        entry_point = REGISTRY[self.main_command]["entry-point"]
        class_instance = class_name()
        self.class_call = getattr(class_instance, entry_point)

    def application(self) -> str:
        # check if entered command is verily a command
        if (self.first_element.type != "COMMAND") or (len(self.commands) == 0):
            raise SyntaxError(f"{self.first_element} не является командой!")

        # match aliases with full flags and make a unified list of them
        local_flags = REGISTRY[self.first_element.value]['flags']
        local_aliases = REGISTRY[self.first_element.value]['aliases']
        for short_flag in self.unique_short_flags:
            short_flag_alias = local_aliases.get(short_flag)
            if short_flag_alias == None:
                raise AttributeError(
                    f"Команда {self.main_command} не имеет флаг -{short_flag}!")
            elif short_flag_alias not in self.long_flags:
                self.long_flags.append(short_flag_alias)

        result = self.class_call(self.long_flags, self.parameters)
        return result  # for now

# Tests to make
# Entering wrong short flag
# Entering wrong long flag


# result = Applicator().application()
# print(result)
