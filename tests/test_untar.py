from src.shell.shell import Shell
import pytest
from unittest.mock import patch
import os
import tarfile
import src.infrastructure.constants as constants


def test_untar_help(fs, setup_fake_environment, reload_untar_module):
    # Call
    shell = Shell()
    result = shell.shell("untar --help")

    # Required value
    expected_help = """Command untar.
Untar zip archives.
Supports 1 flags:
--help
Supports 0 aliases
"""

    # Comparison
    assert result == expected_help


def test_untar_no_parameters_given_error(fs, setup_fake_environment, reload_untar_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("untar")

    assert str(exception.value) == "untar: No parameters were given."


def test_untar_unpack_the_archive(fs, setup_fake_environment, reload_untar_module):
    # Prepare
    archive_path = os.path.join(constants.CURRENT_DIR, "test_archive.tar.gz")
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(os.path.join(constants.CURRENT_DIR, "file42"), arcname="file42")

    # Call
    shell = Shell()
    result = shell.shell("untar test_archive.tar.gz")

    # Comparison
    assert result == "Successfully untarred file test_archive.tar.gz."


def test_untar_unpack_multiple_archives(fs, setup_fake_environment, reload_untar_module):
    # Prepare
    archive1_path = os.path.join(constants.CURRENT_DIR, "test_archive1.tar.gz")
    with tarfile.open(archive1_path, "w:gz") as tar:
        tar.add(os.path.join(constants.CURRENT_DIR, "file42"), arcname="file42")
    archive2_path = os.path.join(constants.CURRENT_DIR, "test_archive2.tar.gz")
    with tarfile.open(archive2_path, "w:gz") as tar:
        tar.add(os.path.join(constants.CURRENT_DIR, "file42"), arcname="file42")

    # Call
    shell = Shell()
    result = shell.shell("untar test_archive1.tar.gz test_archive2.tar.gz")

    # Comparison
    assert result == "Successfully untarred file test_archive1.tar.gz.\nSuccessfully untarred file test_archive2.tar.gz."


def test_untar_nonexistent_archive_error(fs, setup_fake_environment, reload_untar_module):
    # Call
    shell = Shell()
    result = shell.shell("untar nonexistent_archive.tar.gz")

    # Comparison
    assert result == "untar: nonexistent_archive.tar.gz doesn't exist!"


def test_untar_unaccessible_archive_error(fs, setup_fake_environment, reload_untar_module):
    # Prepare
    archive_path = os.path.join(
        constants.CURRENT_DIR, "restricted_archive.tar.gz")
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(os.path.join(constants.CURRENT_DIR, "file42"), arcname="file42")

    # Call
    shell = Shell()

    def mock_access(path, mode):
        if "restricted_archive.tar.gz" in str(path):
            return False
        return os.access(path, mode)

    with patch("os.access", side_effect=mock_access):
        result = shell.shell("untar restricted_archive.tar.gz")

    # Comparison
    assert result == "untar: Can't access restricted_archive.tar.gz!"


def test_untar_archive_is_not_an_archive_error(fs, setup_fake_environment, reload_untar_module):
    # Call
    shell = Shell()
    result = shell.shell("untar file42")

    # Comparison
    assert result == "untar: Can't untar file42. It isn't an archive!"


def test_untar_os_error(fs, setup_fake_environment, reload_untar_module):
    # Prepare
    archive_path = os.path.join(
        constants.CURRENT_DIR, "test_archive_error.tar.gz")
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(os.path.join(constants.CURRENT_DIR, "file42"), arcname="file42")

    # Call
    shell = Shell()

    def mock_extractall(path, members=None, numeric_owner=False):
        raise OSError("Permission denied")

    with patch.object(tarfile.TarFile, "extractall", side_effect=mock_extractall):
        result = shell.shell("untar test_archive_error.tar.gz")

    # Comparison
    assert result == "Unable to untar test_archive_error.tar.gz!"
