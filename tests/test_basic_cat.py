import os
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from src.shell.shell import Shell
import src.infrastructure.constants as constants


def test_cat_help_call(fs: FakeFilesystem):
    # Act
    command = "cat --help"
    shell = Shell()
    result = shell.shell(command)

    # Assert
    assert result.strip() == "cat display file's content."


def test_cat_help_call(fs: FakeFilesystem):
    # Act
    command = "cat --help"
    shell = Shell()
    result = shell.shell(command)

    # Assert
    assert result.strip() == "cat display file's content."


def test_cat_no_parameters(fs: FakeFilesystem):
    # Act
    shell = Shell()
    with pytest.raises(SyntaxError, match="cat: No parameters were given."):
        shell.shell("cat")


def test_cat_folder_listing(fs: FakeFilesystem):
    # Arrange
    fs.create_dir("/folder")
    constants.CURRENT_DIR = os.path.normpath("/")

    # Act
    command = "cat /folder"
    shell = Shell()
    result = shell.shell(command)

    # Assert
    assert result.strip(
    ) == "cat: folder can't be displayed. It's a directory!"


def test_cat_file_listing(fs: FakeFilesystem):
    # Arrange
    fs.create_file("/file", contents="text")

    # Act
    command = "cat /file"
    shell = Shell()
    result = shell.shell(command)

    # Assert
    assert result.strip() == "text"


# def test_cat_for_folder(service: OSConsoleServiceBase, fs: FakeFilesystem):
#     fs.create_dir("data")
#     fs.create_file(os.path.join("data", "existing.txt"), contents="test")

#     with pytest.raises(IsADirectoryError):
#         service.cat("data", mode=FileReadMode.string)


# def test_cat_file_with_text(service: OSConsoleServiceBase, fs: FakeFilesystem):
#     fs.create_dir("data")
#     content = "test"
#     path = os.path.join("data", "existing.txt")
#     fs.create_file(path, contents=content)

#     result = service.cat(path, mode=FileReadMode.string)

#     assert result == content


# def test_cat_file_with_bytes(service: OSConsoleServiceBase, fs: FakeFilesystem):
#     fs.create_dir("data")
#     content = b"test"
#     path = os.path.join("data", "existing.txt")
#     fs.create_file(path, contents=content)

#     result = service.cat(path, mode=FileReadMode.bytes)
#     assert result == content
