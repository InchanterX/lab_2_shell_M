import importlib.util
from pathlib import Path
import importlib

file_paths = list(Path("src/core").rglob("*.py"))
file_paths = [path for path in file_paths if path.is_file()
              and path.suffix == ".py"]

commands = {}

for file_path in file_paths:
    module_name = file_path.stem
    module_path = file_path.resolve()

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, "COMMAND_INFO"):
        module_information = module.COMMAND_INFO
        commands[module_information["name"]] = module_information
    else:
        print(
            f"Модуль {module_name} некорректна и не содержит параметр COMMAND_INFO!")
        pass

print(commands)
