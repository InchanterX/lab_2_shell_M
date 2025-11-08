import src.infrastructure.constants as constants
from src.shell.shell import Shell
import pytest


def test_ls_help(fs, setup_fake_environment, reload_ls_module):
    # Call
    shell = Shell()
    result = shell.shell("ls --help")

    # Required value
    expected_help = """Command ls.
List files in the given folder.
Supports 3 flags:
--all
--long
--help
Supports 2 aliases
-a -l"""

    # Comparison
    assert result == expected_help


def test_ls_current_dir(fs, setup_fake_environment, reload_ls_module):
    # Call
    shell = Shell()
    result = shell.shell("ls")

    # Comparison
    assert "folder1" in result
    assert "folder3" in result
    assert ".folder2" not in result


def test_ls_folder(fs, setup_fake_environment, reload_ls_module):
    # Call
    shell = Shell()
    result = shell.shell("ls folder1")

    # Comparison
    assert result == "folder11   file1   file2"


def test_ls_all_flag(fs, setup_fake_environment, reload_ls_module):
    # Call
    shell = Shell()
    result = shell.shell("ls --all")

    # Comparison
    assert "folder1" in result
    assert "folder3" in result
    assert ".folder2" in result


def test_ls_long_flag(fs, setup_fake_environment, reload_ls_module):
    # Call
    shell = Shell()
    result = shell.shell("ls --long")

    assert "folder1" in result
    lines = result.split("\n")
    assert len(lines) > 1


def test_ls_invalid_path_error(fs, setup_fake_environment, reload_ls_module):
    # Call
    shell = Shell()
    result = shell.shell("ls nonexistent_folder")

    # Comparison
    assert result == "ls: Path nonexistent_folder is invalid!"


def test_ls_file(fs, setup_fake_environment, reload_ls_module):
    # Call
    shell = Shell()
    result = shell.shell("ls file42")

    # Comparison
    assert result == "ls: file42 can't be listed. It's a file!"


def test_ls_invalid_flag_exception(fs, setup_fake_environment, reload_ls_module):
    # Unknown flag
    # Call
    shell = Shell()
    with pytest.raises(AttributeError) as exception:
        shell.shell("ls -h")

    # Comparison
    assert "don't have flag" in str(exception.value)
    assert exception.type is AttributeError


def test_ls_invalid_command_exception():
    # Tokenizer extra check
    # Call
    shell = Shell()
    with pytest.raises(SyntaxError) as exception:
        shell.shell("nonexistent_command")

    # Comparison
    assert str(
        exception.value) == "Command must start with a command name. nonexistent_command is not a command!"
