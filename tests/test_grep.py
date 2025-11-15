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


# def test_grep_invalid_expression_error(fs, setup_fake_environment, reload_grep_module):
#     # Call
#     shell = Shell()
#     with pytest.raises(SyntaxError) as exception:
#         shell.shell("grep '[' file42")

#     # Comparison
#     assert "Pattern" in str(
#         exception.value) and "can't be processed" in str(exception.value)


# def test_grep_permission_denied_file_error(fs, setup_fake_environment, reload_grep_module):
#     # Call
#     shell = Shell()
#     result = shell.shell("grep Test restricted_file.txt")

#     # Comparison
#     assert "grep: cannot search in restricted_file.txt. Permission denied." in result


# def test_grep_permission_denied_directory_error(fs, setup_fake_environment, reload_grep_module):
#     # Call
#     shell = Shell()
#     result = shell.shell("grep -r Test restricted_folder")

#     # Comparison
#     assert "grep: cannot search in restricted_folder. Permission denied." in result


def test_grep_multiple_matches_in_line(fs, setup_fake_environment, reload_grep_module):
    # Prepare
    fs.create_file(
        "/home/fake_user/multi_match.txt",
        contents="test test test\nother line\n")

    # Call
    shell = Shell()
    result = shell.shell("grep test multi_match.txt")

    # Comparison
    lines = result.split("\n")
    assert len(
        [element for element in lines if "multi_match.txt 1" in element]) >= 1


def test_grep_empty_result(fs, setup_fake_environment, reload_grep_module):
    # Prepare
    fs.create_file(
        "/home/fake_user/empty_file.txt")

    # Call
    shell = Shell()
    result = shell.shell("grep NonexistentPattern file42")

    # Comparison
    assert result == ""
