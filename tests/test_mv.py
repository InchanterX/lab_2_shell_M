from src.shell.shell import Shell
import pytest
import os
import src.infrastructure.constants as constants


def test_mv_help(fs, setup_fake_environment, reload_mv_module):
    # Call
    shell = Shell()
    result = shell.shell("mv --help")

    # Required value
    expected_help = """Command mv.
Display file content.
Supports 1 flags:
--help
Supports 0 aliases
"""

    # Comparison
    assert result == expected_help


def test_mv_no_parameters_were_given_error(fs, setup_fake_environment, reload_mv_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("mv")

    assert str(exception.value) == "mv: No parameters were given."


def test_mv_one_parameter_given_error(fs, setup_fake_environment, reload_mv_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("mv file42")

    assert str(exception.value) == "mv: Not enough parameters were given."


def test_mv_invalid_target_folder_error(fs, setup_fake_environment, reload_mv_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("mv file42 folder1/file1 nonexistent_folder")

    assert str(exception.value) == "mv: target nonexistent_folder is invalid!"


def test_mv_rename_a_file(fs, setup_fake_environment, reload_mv_module):
    # Call
    shell = Shell()
    result = shell.shell("mv file42 new_file42")

    # Comparison
    assert result == ""
    assert os.path.exists(os.path.join(constants.CURRENT_DIR, "new_file42"))
    assert not os.path.exists(os.path.join(constants.CURRENT_DIR, "file42"))


def test_mv_rename_nonexistent_file_error(fs, setup_fake_environment, reload_mv_module):
    # Call
    shell = Shell()
    result = shell.shell("mv nonexistent_file new_file")

    # Comparison
    assert result == "mv: nonexistent_file doesn't exist!"


def test_mv_move_file_to_folder(fs, setup_fake_environment, reload_mv_module):
    # Call
    shell = Shell()
    result = shell.shell("mv file42 folder3")

    # Comparison
    assert result == ""
    assert os.path.exists(os.path.join(
        constants.CURRENT_DIR, "folder3", "file42"))
    assert not os.path.exists(os.path.join(constants.CURRENT_DIR, "file42"))


def test_mv_move_multiple_files_to_folder(fs, setup_fake_environment, reload_mv_module):
    # Call
    shell = Shell()
    result = shell.shell("mv folder1/file1 folder1/file2 folder3")

    # Comparison
    assert result == ""
    assert os.path.exists(os.path.join(
        constants.CURRENT_DIR, "folder3", "file1"))
    assert os.path.exists(os.path.join(
        constants.CURRENT_DIR, "folder3", "file2"))


def test_mv_move_nonexistent_file_error(fs, setup_fake_environment, reload_mv_module):
    # Call
    shell = Shell()
    result = shell.shell("mv nonexistent_file folder3")

    # Comparison
    assert result == "mv: nonexistent_file doesn't exist!"
