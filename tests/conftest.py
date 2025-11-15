import os
import sys
import pytest
import importlib
import tarfile
import zipfile
import src.infrastructure.constants as constants

# Enabling pyfakefs pytest plugin
pytest_plugins = ["pyfakefs"]


def _create_project_dir_in_fakefs(fake_fs):
    '''
    Create project dir in fake filesystem
    '''
    real_project_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), ".."))

    try:
        if not fake_fs.exists(real_project_dir):
            parts = real_project_dir.split(os.sep)
            if parts[0] == '':
                current_path = os.sep
                parts = parts[1:]
            else:
                current_path = parts[0]
                parts = parts[1:]

            for part in parts:
                if part:
                    current_path = os.path.join(current_path, part)
                    if not fake_fs.exists(current_path):
                        fake_fs.create_dir(current_path)
    except Exception:
        pass


@pytest.fixture(scope="function", autouse=True)
def setup_real_project_dir_in_fs(fs):
    '''
    Ensure directory existence.
    '''
    _create_project_dir_in_fakefs(fs)


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
        raise ValueError(f"Unknown command: {command_name}.")

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
    '''Fixture to reloads cd module.'''
    return _reload_command_module("cd")


@pytest.fixture
def reload_cat_module():
    '''Fixture to reloads cat module.'''
    return _reload_command_module("cat")


@pytest.fixture
def reload_cp_module():
    '''Fixture to reloads cp module.'''
    return _reload_command_module("cp")


@pytest.fixture
def reload_mv_module():
    '''Fixture to reloads mv module.'''
    return _reload_command_module("mv")


@pytest.fixture
def reload_rm_module():
    '''Fixture to reloads rm module.'''
    return _reload_command_module("rm")


@pytest.fixture
def reload_tar_module():
    '''Fixture to reloads tar module.'''
    return _reload_command_module("tar")


@pytest.fixture
def reload_untar_module():
    '''Fixture to reloads untar module.'''
    return _reload_command_module("untar")


@pytest.fixture
def reload_zip_module():
    '''Fixture to reloads zip module.'''
    return _reload_command_module("zip")


@pytest.fixture
def reload_unzip_module():
    '''Fixture to reloads unzip module.'''
    return _reload_command_module("unzip")


@pytest.fixture
def reload_example_module():
    '''Fixture to reload example module.'''
    return _reload_command_module("example")


@pytest.fixture
def reload_pwd_module():
    '''Fixture to reload pwd module.'''
    return _reload_command_module("pwd")


@pytest.fixture
def reload_grep_module():
    '''Fixture to reload grep module.'''
    return _reload_command_module("grep")


@pytest.fixture
def reload_history_module():
    '''Fixture to reload history module.'''
    return _reload_command_module("history")


@pytest.fixture
def reload_undo_module():
    '''Fixture to reload undo module.'''
    return _reload_command_module("undo")


@pytest.fixture
def setup_fake_environment(fs):
    '''
    Automatically setup fake environment by editing constants and creating files and folders for tests.
    '''

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

    # prepare paths for history and trash dirs and files in fake filesystem
    project_root = os.path.join(base_directory, "project_root")
    history_dir = os.path.join(project_root, ".history")
    trash_dir = os.path.join(project_root, ".trash")
    history_path = os.path.join(history_dir, "history.json")

    # creating history and trash files and dirs
    fs.create_dir(project_root)
    fs.create_dir(history_dir)
    fs.create_dir(trash_dir)
    fs.create_file(
        history_path, contents='{\n  "meta": {\n    "last_reversible_id": 0\n  },\n  "records": []\n}')

    # replacing constants values
    constants.USER_HOME_DIR = home_directory
    constants.CURRENT_DIR = current_directory
    constants.LOG_DIR = logging_directory
    constants.USER_LOGIN = "fake_user"
    constants.HISTORY_PATH = history_path
    constants.TRASH_DIR = trash_dir

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
    fs.create_file(f"{current_directory}/file42", contents="Test_information.")

    # Creating binary file
    fs.create_file(
        f"{current_directory}/binary_file.bin", contents=b"\x80\x81\x82\x83\xff\xfe\xfd"
    )

    # Creating files with changed permissions
    fs.create_file(
        f"{current_directory}/restricted_file.txt", contents="Restricted content"
    )
    fs.chmod(f"{current_directory}/restricted_file.txt", 0o000)
    fs.create_dir(
        f"{current_directory}/restricted_folder"
    )
    fs.create_file(f"{current_directory}/restricted_folder/file23.pdf")
    fs.chmod(f"{current_directory}/restricted_folder", 0o000)

    # Creating folders for coping|moving|removing tests
    fs.create_dir(f"{current_directory}/empty_folder")
    fs.create_dir(f"{current_directory}/test_folder")
    fs.create_file(
        f"{current_directory}/test_folder/test_file", contents="test")
    fs.create_dir(f"{current_directory}/test_folder2")
    fs.create_file(
        f"{current_directory}/test_folder2/test_file", contents="test")
    fs.create_dir(f"{current_directory}/test_folder3")
    fs.create_file(
        f"{current_directory}/test_folder3/test_file", contents="test")
    fs.create_dir(f"{current_directory}/test_folder4")
    fs.create_file(
        f"{current_directory}/test_folder4/test_file", contents="test")
    fs.create_file(f"{current_directory}/restricted_file.tar.gz",
                   contents="test content")
    fs.create_file(f"{current_directory}/restricted_file.zip",
                   contents="test content")

    # Create archives for zip and tar tests
    with tarfile.open(f"{current_directory}/archive.tar.gz", "w:gz") as tar:
        tar.add(f"{current_directory}/file42", arcname="file42")
    with zipfile.ZipFile(f"{current_directory}/archive.zip", "w") as zip_file:
        zip_file.write(f"{current_directory}/file42", arcname="file42")

    yield
