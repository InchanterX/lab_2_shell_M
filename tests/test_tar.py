from src.shell.shell import Shell
import pytest
from unittest.mock import patch
import os
import tarfile
import src.infrastructure.constants as constants


def test_tar_help(fs, setup_fake_environment, reload_tar_module):
    # Call
    shell = Shell()
    result = shell.shell("tar --help")

    # Required value
    expected_help = """Command tar.
Tar given files.
Supports 1 flags:
--help
Supports 0 aliases
"""

    # Comparison
    assert result == expected_help


def test_tar_no_parameters_given_error(fs, setup_fake_environment, reload_tar_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("tar")

    assert str(exception.value) == "tar: No parameters were given."


def test_tar_create_archive_with_file(fs, setup_fake_environment, reload_tar_module):
    # Call
    shell = Shell()
    result = shell.shell("tar file42")

    # Comparison
    assert result == "Successfully added folder file42 to \"archive1.tar.gz\"!"


def test_tar_create_archive_with_multiple_files(fs, setup_fake_environment, reload_tar_module):
    # Call
    shell = Shell()
    result = shell.shell("tar file42 folder1/file1")

    # Comparison
    assert result == "Successfully added folder file42 to \"archive1.tar.gz\"!\nSuccessfully added folder folder1/file1 to \"archive1.tar.gz\"!"


def test_tar_create_archive_with_folder(fs, setup_fake_environment, reload_tar_module):
    # Call
    shell = Shell()
    result = shell.shell("tar folder1")

    # Comparison
    assert result == "Successfully added folder folder1 to \"archive1.tar.gz\"!"


def test_tar_archive_names_collisions(fs, setup_fake_environment, reload_tar_module):
    # Call
    shell = Shell()
    result = shell.shell("tar file42")

    # Comparison
    assert result == "Successfully added folder file42 to \"archive1.tar.gz\"!"
    assert os.path.exists(os.path.join(
        constants.CURRENT_DIR, "archive1.tar.gz"))


def test_tar_nonexistent_file_error(fs, setup_fake_environment, reload_tar_module):
    # Call
    shell = Shell()
    result = shell.shell("tar nonexistent_file")

    # Comparison
    assert result == "tar: nonexistent_file doesn't exist!"


def test_tar_unaccessible_file_error(fs, setup_fake_environment, reload_tar_module):
    # Call
    shell = Shell()

    def mock_access(path, mode):
        if "restricted_file.tar.gz" in str(path):
            return False
        return os.access(path, mode)

    with patch("os.access", side_effect=mock_access):
        result = shell.shell("tar restricted_file.tar.gz")

    # Comparison
    assert result == "tar: Can't access restricted_file.tar.gz!"


def test_tar_os_error(fs, setup_fake_environment, reload_tar_module):
    # Call
    shell = Shell()

    def mock_add(name, arcname=None, recursive=True, filter=None):
        raise OSError("Permission denied")

    with patch.object(tarfile.TarFile, "add", side_effect=mock_add):
        result = shell.shell("tar file42")

    # Comparison
    assert result == "Unable to zip file42!"
