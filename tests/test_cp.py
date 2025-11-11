from src.shell.shell import Shell
import pytest


def test_cp_help(fs, setup_fake_environment, reload_cd_module):
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


def test_cp_no_parameters_given_error(fs, setup_fake_environment, reload_cat_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("cp")

    assert str(exception.value) == "cp: No parameters were given."


def test_cp_one_parameter_given_error(fs, setup_fake_environment, reload_cat_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("cp file42")

    assert str(exception.value) == "cp: Not enough parameters were given."


def test_cp_file_plus_file_given_error(fs, setup_fake_environment, reload_cat_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("cp file42 folder1/file1")

    assert str(
        exception.value) == "cp: folder path folder1/file1 is incorrect!"


def test_one_file_copy(fs, setup_fake_environment, reload_cat_module):
    # Call
    shell = Shell()
    result = shell.shell("cp file42 folder1")

    assert result == "Copied folder file42 to folder1."
