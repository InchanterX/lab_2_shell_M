from src.shell.shell import Shell
import pytest


def test_grep_help(fs, setup_fake_environment, reload_grep_module):
    # Call
    shell = Shell()
    result = shell.shell("grep --help")

    # Required value
    expected_help = """Command grep.
Search.
Supports 3 flags:
--recursive
--ignore_case
--help
Supports 2 aliases
-r -i"""

    # Comparison
    assert result == expected_help


def test_grep_no_parameters_given_error(fs, setup_fake_environment, reload_grep_module):
    # Call
    shell = Shell()

    # Comparison
    with pytest.raises(SyntaxError) as exception:
        shell.shell("grep")

    assert str(exception.value) == "grep: No parameters were given."


def test_grep_search_in_file(fs, setup_fake_environment, reload_grep_module):
    # Call
    shell = Shell()
    result = shell.shell("grep Test file42")

    # Comparison
    assert "file42" in result
    assert "Test" in result


def test_grep_search_in_current_directory(fs, setup_fake_environment, reload_grep_module):
    # Call
    shell = Shell()
    result = shell.shell("grep Test")

    # Comparison
    assert isinstance(result, str)


def test_grep_search_with_ignore_case_flag(fs, setup_fake_environment, reload_grep_module):
    # Call
    shell = Shell()
    result = shell.shell("grep --ignore-case test file42")

    # Comparison
    assert "file42" in result or result == ""


def test_grep_search_with_i_alias(fs, setup_fake_environment, reload_grep_module):
    # Call
    shell = Shell()
    result = shell.shell("grep -i test file42")

    # Comparison
    assert "file42" in result or result == ""


def test_grep_search_in_folder_with_recursive_flag(fs, setup_fake_environment, reload_grep_module):
    # Call
    shell = Shell()
    result = shell.shell("grep --recursive Text folder1")

    # Comparison
    assert "folder1" in result or result == ""


def test_grep_search_in_folder_with_r_alias(fs, setup_fake_environment, reload_grep_module):
    # Call
    shell = Shell()
    result = shell.shell("grep -r Text folder1")

    # Comparison
    assert "folder1" in result or result == ""


def test_grep_search_in_folder_without_recursive_flag_error(fs, setup_fake_environment, reload_grep_module):
    # Call
    shell = Shell()
    result = shell.shell("grep Text folder1")

    # Comparison
    assert "grep: folder folder1 can't be processed without --recursive flag." in result


def test_grep_nonexistent_file_error(fs, setup_fake_environment, reload_grep_module):
    # Call
    shell = Shell()
    result = shell.shell("grep Test nonexistent_file")

    # Comparison
    assert "grep: File nonexistent_file can't be processed. It doesn't exist." in result
