import os
import sys
import pytest
import importlib
import src.infrastructure.constants as constants

# Enabling pyfakefs pytest plugin
pytest_plugins = ["pyfakefs"]


def _gather_command_modules():
    '''
    Dynamically prepare list of modules from REGISTRY
    '''
    command_modules = {}

    # Extra check to prevent exceptions
    if not constants.REGISTRY:
        importlib.reload(constants)

    # importing all commands
    command_names = list(constants.REGISTRY.keys())
    for command_name in command_names:
        commands_module_path = f"src.core.commands.{command_name}"
        user_commands_module_path = f"src.core.user_commands.{command_name}"

        # try to find command in basic commands
        try:
            importlib.import_module(commands_module_path)
            module_path = commands_module_path
        # otherwise import it from the users commands
        except ImportError:
            module_path = user_commands_module_path

        command_modules[command_name] = module_path

    return command_modules


# Cache the command modules map
is_module_was_imported = None


def _get_command_modules():
    '''Reload module if it is necessary'''
    global is_module_was_imported

    # Again extra check to prevent exceptions
    if not constants.REGISTRY:
        importlib.reload(constants)

    if is_module_was_imported is None:
        is_module_was_imported = _gather_command_modules()
    return is_module_was_imported


def _reload_command_module(command_name: str):
    '''
    Function that helps to reload command modules and registry not to loose them during testing.
    '''
    # Get all dynamic command modules
    command_modules = _get_command_modules()

    if command_name not in command_modules:
        raise ValueError(
            f"Unknown command: {command_name}."
        )

    module_path = command_modules[command_name]

    # import/reload module
    if module_path in sys.modules:
        module = importlib.reload(sys.modules[module_path])
    else:
        module = importlib.import_module(module_path)

    # reload registry
    COMMAND_INFO = getattr(module, "COMMAND_INFO")
    constants.REGISTRY[command_name] = COMMAND_INFO

    return module


@pytest.fixture
def reload_ls_module():
    '''Fixture to reloads basic_ls module.'''
    return _reload_command_module("ls")


@pytest.fixture
def reload_cd_module():
    '''Fixture to reloads basic_cd module.'''
    return _reload_command_module("cd")


@pytest.fixture
def reload_cat_module():
    '''Fixture to reloads basic_cat module.'''
    return _reload_command_module("cat")


@pytest.fixture
def setup_fake_environment(fs):
    """
    Automatically setup fake environment by editing constants and creating files and folders for tests.
    """

    # creating base depending on the current os
    if os.name == "nt":
        base_directory = "C:\\"
        fs.add_mount_point(base_directory)
    else:
        base_directory = "/"

    # creating fake os base
    home_directory = os.path.join(base_directory, "home", "fake_user")
    current_directory = home_directory
    logging_directory = os.path.join(base_directory, "logs")

    fs.create_dir(home_directory)
    fs.create_dir(logging_directory)

    # replacing constants values
    constants.USER_HOME_DIR = home_directory
    constants.CURRENT_DIR = current_directory
    constants.LOG_DIR = logging_directory
    constants.USER_LOGIN = "fake_user"

    # creating basic testing folders and files
    fs.create_dir(f"{current_directory}/folder1")
    fs.create_dir(f"{current_directory}/folder1/folder11")
    fs.create_file(
        f"{current_directory}/folder1/folder11/file11", contents="Text")
    fs.create_file(f"{current_directory}/folder1/file1")
    fs.create_file(f"{current_directory}/folder1/file2",
                   contents="Some testing text")
    fs.create_dir(f"{current_directory}/.folder2")
    fs.create_dir(f"{current_directory}/.folder2/file2")
    fs.create_dir(f"{current_directory}/folder3")
    fs.create_file(f"{current_directory}/file42")
    yield
