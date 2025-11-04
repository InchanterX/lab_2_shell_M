import importlib.util
from pathlib import Path
from typing import Any
import importlib
import logging


class Registry:
    '''
    Registry create a registry of all available commands by searching validly written files in src/core folder.
    If file contains basic structure, especially it contains configuration variable - it is valid and will be to registry.
    Returns tuple with all the commands and information about them.
    '''

    def __init__(self, basic_directory: str = "src/core") -> None:
        self.basic_directory = Path(basic_directory)
        self.commands: dict[str, dict[str, Any]] = {}
        self._logger = logging.getLogger(__name__)

    def registration(self) -> tuple[bool, dict[str, dict[str, Any]]]:

        try:
            # search for python files in the src/core
            file_paths = [file_path for file_path in Path(
                "src/core").rglob("*.py") if not file_path.name.startswith("__")]

            commands = {}

            # process every found file
            for file_path in file_paths:
                module_name = file_path.stem
                module_path = file_path.resolve()

                # load and import files to extract config
                spec = importlib.util.spec_from_file_location(
                    module_name, module_path)

                # check the existence of spec
                if spec is None:
                    self._logger.warning(
                        f"Couldn't load spec for module {module_name}.")
                    continue

                # check the existence of loader
                if spec.loader is None:
                    self._logger.warning(
                        f"Couldn't load spec for module {module_name}, there is no loader.")
                    continue

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # get config if there is such
                if hasattr(module, "COMMAND_INFO"):
                    module_information = module.COMMAND_INFO
                    commands[module_information["name"]] = module_information
                # otherwise skips the file and continue
                else:
                    self._logger.warning(
                        f"Module {module_name} is invalid. There is no configuration attribute COMMAND_INFO in the file. It won't be loaded.")
                    print(
                        f"Module {module_name} wasn't loaded, see .log files for more information.")
        except Exception:
            print("Surprise awaits you in the log file.")
            self._logger.fatal(
                "If you see this error, it means that there is a fundamental problem in generating registry. Check the state of the src/code folder and files completeness.")
            raise AttributeError("This project is ass.")

        return True, commands
