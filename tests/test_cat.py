from src.shell.shell import Shell
import pytest
from unittest.mock import patch


def test_cat_help(fs, setup_fake_environment, reload_cat_module):
    # Call
    shell = Shell()
    result = shell.shell("cat --help")

    # Required value
    expected_help = """Command cat.
Display file content.
Supports 1 flags:
--help
Supports 0 aliases
"""

    # Comparison
    assert result == expected_help


def test_cat_no_parameters_given(fs, setup_fake_environment, reload_cat_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("cat")

    assert str(exception.value) == "cat: No parameters were given."


def test_cat_dir_was_given(fs, setup_fake_environment, reload_cat_module):
    # Call
    shell = Shell()
    result = shell.shell("cat folder1")

    # Comparison
    assert result == "cat: folder1 can't be displayed. It's a directory!"


def test_cat_file_was_given(fs, setup_fake_environment, reload_cat_module):
    # Call
    shell = Shell()
    result = shell.shell("cat file42")

    # Comparison
    assert result == "Test_information."


def test_cat_several_parameters(fs, setup_fake_environment, reload_cat_module):
    # Call
    shell = Shell()
    result = shell.shell("cat folder1 file42")

    # Comparison
    assert (
        result
        == "cat: folder1 can't be displayed. It's a directory!\nTest_information."
    )


def test_cat_unicode_decode_error(fs, setup_fake_environment, reload_cat_module):
    # Call
    shell = Shell()
    result = shell.shell("cat binary_file.bin")

    # Comparison
    assert result == "cat: cannot display binary file binary_file.bin!"


def test_cat_permission_error(fs, setup_fake_environment, reload_cat_module):
    # Call
    shell = Shell()

    def mock_open(file_path, *args, **kwargs):
        if "restricted_file.txt" in str(file_path):
            raise PermissionError("Permission denied")
        return open(file_path, *args, **kwargs)

    with patch("builtins.open", side_effect=mock_open):
        result = shell.shell("cat restricted_file.txt")

    # Comparison
    assert result == "cat: cannot access restricted_file.txt!"


def test_cat_incorrect_path_given(fs, setup_fake_environment, reload_cat_module):
    # Call
    shell = Shell()
    result = shell.shell("cat nonexistence_file")

    # Comparison
    assert result == "cat: file nonexistence_file does not exist!"
