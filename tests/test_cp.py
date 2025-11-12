from src.shell.shell import Shell
import pytest
from unittest.mock import patch


def test_cp_help(fs, setup_fake_environment, reload_cp_module):
    # Call
    shell = Shell()
    result = shell.shell("cp --help")

    # Required value
    expected_help = """Command cp.
Copy files to a different folder.
Supports 2 flags:
--recursive
--help
Supports 1 aliases
-r"""

    # Comparison
    assert result == expected_help


def test_cp_no_parameters_given_error(fs, setup_fake_environment, reload_cp_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("cp")

    assert str(exception.value) == "cp: No parameters were given."


def test_cp_one_parameter_given_error(fs, setup_fake_environment, reload_cp_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("cp file42")

    assert str(exception.value) == "cp: Not enough parameters were given."


def test_cp_file_plus_file_given_error(fs, setup_fake_environment, reload_cp_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("cp file42 folder1/file1")

    assert str(exception.value) == "cp: folder path folder1/file1 is incorrect!"


def test_one_file_copy(fs, setup_fake_environment, reload_cp_module):
    # Call
    shell = Shell()
    result = shell.shell("cp file42 folder3")

    assert result == "Copied file file42 to folder3."


def test_cp_multiple_files_copy(fs, setup_fake_environment, reload_cp_module):
    # Call
    shell = Shell()
    result = shell.shell("cp file42 folder1/file1 folder3")

    # Comparison
    assert result == "Copied file file42 to folder3.\nCopied file folder1/file1 to folder3."


def test_cp_coping_folder_without_recursive_flag_error(fs, setup_fake_environment, reload_cp_module):
    # Call
    shell = Shell()
    result = shell.shell("cp folder1 folder3")

    # Comparison
    assert result == "cp: you can't copy folder folder1 without flag [-r|--recursive]."


def test_cp_coping_folder_with_recursive_flag(fs, setup_fake_environment, reload_cp_module):
    # Call
    shell = Shell()
    result = shell.shell("cp --recursive folder1 folder3")

    # Comparison
    assert result == "Copied folder folder1 to folder3."


def test_cp_coping_folder_with_recursive_flag_alias(fs, setup_fake_environment, reload_cp_module):
    # Call
    shell = Shell()
    result = shell.shell("cp -r folder1 folder3")

    # Comparison
    assert result == "Copied folder folder1 to folder3."


def test_cp_coping_nonexistent_file_error(fs, setup_fake_environment, reload_cp_module):
    # Call
    shell = Shell()
    result = shell.shell("cp nonexistent_file folder3")

    # Comparison
    assert result == "cp: failed to copy nonexistent_file. It doesn't exist."


def test_cp_coping_file_exception(fs, setup_fake_environment, reload_cp_module):
    # Call
    shell = Shell()

    def mock_copyfile(*args, **kwargs):
        raise OSError("Permission denied")

    with patch("shutil.copyfile", side_effect=mock_copyfile):
        result = shell.shell("cp file42 folder3")

    # Comparison
    assert result == "cp: failed to copy file42."


def test_cp_coping_folder_exception(fs, setup_fake_environment, reload_cp_module):
    # Call
    shell = Shell()

    def mock_copytree(*args, **kwargs):
        raise OSError("Permission denied")

    with patch("shutil.copytree", side_effect=mock_copytree):
        result = shell.shell("cp --recursive folder1 folder3")

    # Comparison
    assert result == "cp: failed to copy folder1."
