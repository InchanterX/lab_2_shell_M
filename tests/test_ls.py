from pyfakefs.fake_filesystem_unittest import Patcher
import os
import src.infrastructure.constants as constants
from pyfakefs.fake_filesystem import FakeFilesystem
from src.shell.shell import Shell


def test_ls_current_dir(fs: FakeFilesystem):
    # creating base depending on the current os
    if os.name == "nt":
        base_directory = "C:\\"
        fs.add_mount_point(base_directory)
        print(fs.is_windows_fs)
    else:
        base_directory = "/"

    # creating fake os base
    home_directory = os.path.join(base_directory, "home", "fake_user")
    current_directory = home_directory
    logging_directory = os.path.join(base_directory, "logs")
    print(home_directory)

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
    print(os.listdir("C:\\home\\fake_user"))

    shell = Shell()
    result = shell.shell("ls")
    assert "folder1" in result
    assert "folder3" in result


fs = FakeFilesystem()
# или — более правильный способ:
with Patcher() as patcher:
    fs = patcher.fs
    test_ls_current_dir(fs)
