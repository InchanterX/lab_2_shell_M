import importlib.util
from pathlib import Path
from typing import Any
import importlib


class Registry:

    def __init__(self, basic_directory: str = "src/core") -> None:
        self.basic_directory = Path(basic_directory)
        self.commands: dict[str, dict[str, Any]] = {}

    def registration(self) -> tuple[bool, dict[str, dict[str, Any]]]:

        try:
            file_paths = [file_path for file_path in Path(
                "src/core").rglob("*.py") if not file_path.name.startswith("__")]

            commands = {}

            for file_path in file_paths:
                module_name = file_path.stem
                module_path = file_path.resolve()

                spec = importlib.util.spec_from_file_location(
                    module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, "COMMAND_INFO"):
                    module_information = module.COMMAND_INFO
                    commands[module_information["name"]] = module_information
                else:
                    pass
                    # !!! Should be replaced with warning!
                    # raise AttributeError("You module is ass.")
                    # print(
                    #     f"Module {module_name} is incorrect, there is no attribute COMMAND_INFO!")
        except:
            raise AttributeError("You module is ass.")
            # !!! Should be replaced with warning!
            # print(f"Failed to register module {module_name} at {module_path}!")

        return commands
