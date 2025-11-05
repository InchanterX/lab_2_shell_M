import os
import pytest
import importlib
import src.infrastructure.constants as constants


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

    print(constants.CURRENT_DIR)
    print(os.listdir(current_directory))

    # # project modules reload
    # importlib.reload(constants)
    # importlib.invalidate_caches()
    yield
