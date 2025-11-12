from src.shell.shell import Shell
import pytest
from unittest.mock import patch
import os
import zipfile
import src.infrastructure.constants as constants


def test_unzip_help(fs, setup_fake_environment, reload_unzip_module):
    # Call
    shell = Shell()
    result = shell.shell("unzip --help")

    # Required value
    expected_help = """Command unzip.
Unzip zip archives.
Supports 1 flags:
--help
Supports 0 aliases
"""

    # Comparison
    assert result == expected_help


def test_unzip_no_parameters_given_error(fs, setup_fake_environment, reload_unzip_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("unzip")

    assert str(exception.value) == "unzip: No parameters were given."


def test_unzip_unpack_the_archive(fs, setup_fake_environment, reload_unzip_module):
    # Prepare
    archive_path = os.path.join(constants.CURRENT_DIR, "test_archive.zip")
    with zipfile.ZipFile(archive_path, "w") as zip_file:
        zip_file.write(os.path.join(constants.CURRENT_DIR, "file42"), arcname="file42")

    # Call
    shell = Shell()
    result = shell.shell("unzip test_archive.zip")

    # Comparison
    assert result == "Successfully unzipped file test_archive.zip."


def test_unzip_unpack_multiple_archives(fs, setup_fake_environment, reload_unzip_module):
    # Prepare
    archive1_path = os.path.join(constants.CURRENT_DIR, "test_archive1.zip")
    with zipfile.ZipFile(archive1_path, "w") as zip_file:
        zip_file.write(os.path.join(constants.CURRENT_DIR, "file42"), arcname="file42")
    archive2_path = os.path.join(constants.CURRENT_DIR, "test_archive2.zip")
    with zipfile.ZipFile(archive2_path, "w") as zip_file:
        zip_file.write(os.path.join(constants.CURRENT_DIR, "file42"), arcname="file42")

    # Call
    shell = Shell()
    result = shell.shell("unzip test_archive1.zip test_archive2.zip")

    # Comparison
    assert result == "Successfully unzipped file test_archive1.zip.\nSuccessfully unzipped file test_archive2.zip."


def test_unzip_nonexistent_archive_error(fs, setup_fake_environment, reload_unzip_module):
    # Call
    shell = Shell()
    result = shell.shell("unzip nonexistent_archive.zip")

    # Comparison
    assert result == "unzip: nonexistent_archive.zip doesn't exist!"


def test_unzip_unaccessible_archive_error(fs, setup_fake_environment, reload_unzip_module):
    # Prepare
    archive_path = os.path.join(constants.CURRENT_DIR, "restricted_archive.zip")
    with zipfile.ZipFile(archive_path, "w") as zip_file:
        zip_file.write(os.path.join(constants.CURRENT_DIR, "file42"), arcname="file42")

    # Call
    shell = Shell()

    def mock_access(path, mode):
        if "restricted_archive.zip" in str(path):
            return False
        return os.access(path, mode)

    with patch("os.access", side_effect=mock_access):
        result = shell.shell("unzip restricted_archive.zip")

    # Comparison
    assert result == "unzip: Can't access restricted_archive.zip!"


def test_unzip_archive_is_not_an_archive_error(fs, setup_fake_environment, reload_unzip_module):
    # Call
    shell = Shell()
    result = shell.shell("unzip file42")

    # Comparison
    assert result == "unzip: Can't unzip file42. It isn't an archive!"


def test_unzip_os_error(fs, setup_fake_environment, reload_unzip_module):
    # Prepare
    archive_path = os.path.join(constants.CURRENT_DIR, "test_archive_error.zip")
    with zipfile.ZipFile(archive_path, "w") as zip_file:
        zip_file.write(os.path.join(constants.CURRENT_DIR, "file42"), arcname="file42")

    # Call
    shell = Shell()

    def mock_extractall(path, members=None, numeric_owner=False):
        raise OSError("Permission denied")

    with patch.object(zipfile.ZipFile, "extractall", side_effect=mock_extractall):
        result = shell.shell("unzip test_archive_error.zip")

    # Comparison
    assert result == "Unable to unzip test_archive_error.zip!"
