from src.shell.shell import Shell
import pytest
from unittest.mock import patch
import os
import zipfile
import src.infrastructure.constants as constants


def test_zip_help(fs, setup_fake_environment, reload_zip_module):
    # Call
    shell = Shell()
    result = shell.shell("zip --help")

    # Required value
    expected_help = """Command zip.
Zip given files.
Supports 1 flags:
--help
Supports 0 aliases
"""

    # Comparison
    assert result == expected_help


def test_zip_no_parameters_were_given_error(fs, setup_fake_environment, reload_zip_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("zip")

    assert str(exception.value) == "zip: No parameters were given."


def test_zip_create_archive_with_file(fs, setup_fake_environment, reload_zip_module):
    # Call
    shell = Shell()
    result = shell.shell("zip file42")

    # Comparison
    assert result == "Successfully added file42 to \"archive1.zip\"!"


def test_zip_create_archive_with_multiple_files(fs, setup_fake_environment, reload_zip_module):
    # Call
    shell = Shell()
    result = shell.shell("zip file42 folder1/file1")

    # Comparison
    assert result == "Successfully added file42 to \"archive1.zip\"!\nSuccessfully added folder1/file1 to \"archive1.zip\"!"


def test_zip_create_archive_with_folder(fs, setup_fake_environment, reload_zip_module):
    # Call
    shell = Shell()
    result = shell.shell("zip folder1")

    # Comparison
    assert result == "Successfully added folder folder1 to \"archive1.zip\"!"


def test_zip_archive_names_collisions(fs, setup_fake_environment, reload_zip_module):
    # Call
    shell = Shell()
    result = shell.shell("zip file42")

    # Comparison
    assert result == "Successfully added file42 to \"archive1.zip\"!"
    assert os.path.exists(os.path.join(constants.CURRENT_DIR, "archive1.zip"))


def test_zip_nonexistent_file_error(fs, setup_fake_environment, reload_zip_module):
    # Call
    shell = Shell()
    result = shell.shell("zip nonexistent_file")

    # Comparison
    assert result == "zip: nonexistent_file doesn't exist!"


def test_zip_unaccessible_file_error(fs, setup_fake_environment, reload_zip_module):
    # Call
    shell = Shell()

    def mock_access(path, mode):
        if "restricted_file.zip" in str(path):
            return False
        return os.access(path, mode)

    with patch("os.access", side_effect=mock_access):
        result = shell.shell("zip restricted_file.zip")

    # Comparison
    assert result == "zip: Can't access restricted_file.zip!"


def test_zip_os_error(fs, setup_fake_environment, reload_zip_module):
    # Call
    shell = Shell()

    def mock_write(path, arcname=None):
        raise OSError("Permission denied")

    with patch.object(zipfile.ZipFile, "write", side_effect=mock_write):
        result = shell.shell("zip file42")

    # Comparison
    assert result == "Unable to zip file42!"
