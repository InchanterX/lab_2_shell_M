from src.shell.shell import Shell
import pytest
from unittest.mock import patch
import os
import shutil


def test_rm_help(fs, setup_fake_environment, reload_rm_module):
    # Call
    shell = Shell()
    result = shell.shell("rm --help")

    # Required value
    expected_help = """Command rm.
Copy files to a different folder.
Supports 3 flags:
--recursive
--force
--help
Supports 2 aliases
-r -f"""

    # Comparison
    assert result == expected_help


def test_rm_no_parameters_were_given_error(fs, setup_fake_environment, reload_rm_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("rm")

    assert str(exception.value) == "rm: No parameters were given."


def test_rm_delete_a_file(fs, setup_fake_environment, reload_rm_module):
    # Call
    shell = Shell()
    result = shell.shell("rm file42")

    # Comparison
    assert result == ""


def test_rm_delete_file_permission_error(fs, setup_fake_environment, reload_rm_module):
    # Call
    shell = Shell()

    def mock_remove(file_path):
        if "restricted_file.txt" in str(file_path):
            raise PermissionError("Permission denied")
        return os.remove(file_path)

    with patch("os.remove", side_effect=mock_remove):
        result = shell.shell("rm restricted_file.txt")

    # Comparison
    assert result == "rm: cannot delete restricted_file.txt. Permission denied."


def test_rm_delete_empty_folder_without_consent(fs, setup_fake_environment, reload_rm_module):
    # Call
    shell = Shell()
    result = shell.shell("rm empty_folder")

    # Comparison
    assert result == ""


def test_rm_delete_folder_without_recursive_flag_error(fs, setup_fake_environment, reload_rm_module):
    # Call
    shell = Shell()

    with patch("builtins.input", return_value="n"):
        result = shell.shell("rm folder1")

    # Comparison
    assert result == "rm: you can't remove the folder folder1 without consent or flag [-r|--recursive]."


def test_rm_delete_folder_with_user_consent(fs, setup_fake_environment, reload_rm_module):
    # Call
    shell = Shell()

    with patch("builtins.input", return_value="y"):
        result = shell.shell("rm test_folder")

    # Comparison
    assert result == ""


def test_rm_delete_folder_with_recursive_flag(fs, setup_fake_environment, reload_rm_module):
    # Call
    shell = Shell()

    with patch("builtins.input", return_value="n"):
        result = shell.shell("rm --recursive folder1")

    # Comparison
    assert result == ""


def test_rm_delete_folder_with_r_alias(fs, setup_fake_environment, reload_rm_module):
    # Call
    shell = Shell()

    with patch("builtins.input", return_value="n"):
        result = shell.shell("rm -r test_folder2")

    # Comparison
    assert result == ""


def test_rm_delete_folder_with_force_flag(fs, setup_fake_environment, reload_rm_module):
    # Call
    shell = Shell()
    result = shell.shell("rm --force test_folder3")

    # Comparison
    assert result == ""


def test_rm_delete_folder_with_force_flag_alias(fs, setup_fake_environment, reload_rm_module):
    # Call
    shell = Shell()
    result = shell.shell("rm -f test_folder4")

    # Comparison
    assert result == ""


def test_rm_delete_nonexistent_file_error(fs, setup_fake_environment, reload_rm_module):
    # Call
    shell = Shell()
    result = shell.shell("rm nonexistent_file")

    # Comparison
    assert result == "rm: failed to delete nonexistent_file. It doesn't exist."


def test_rm_delete_folder_permission_error(fs, setup_fake_environment, reload_rm_module):
    # Call
    shell = Shell()

    def mock_rmtree(folder_path):
        if "restricted_folder" in str(folder_path):
            raise PermissionError("Permission denied")
        return shutil.rmtree(folder_path)

    with patch("shutil.rmtree", side_effect=mock_rmtree), patch("builtins.input", return_value="n"):
        result = shell.shell("rm --recursive restricted_folder")

    # Comparison
    assert result == "rm: cannot delete restricted_folder. Permission denied."


def test_rm_delete_folder_os_error(fs, setup_fake_environment, reload_rm_module):
    # Call
    shell = Shell()

    def mock_rmtree(folder_path):
        raise OSError("Device or resource busy")

    with patch("shutil.rmtree", side_effect=mock_rmtree), patch("builtins.input", return_value="n"):
        result = shell.shell("rm --recursive folder1")

    # Comparison
    assert result == "rm: failed to delete folder1."


def test_rm_delete_prohibited_path(fs, setup_fake_environment, reload_rm_module):
    # Call
    shell = Shell()
    result = shell.shell("rm /")

    # Comparison
    assert "rm: you can't delete /." in result
