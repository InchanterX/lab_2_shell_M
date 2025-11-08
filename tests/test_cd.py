import src.infrastructure.constants as constants
from src.shell.shell import Shell


def test_cd_help(fs, setup_fake_environment, reload_cd_module):
    # Call
    shell = Shell()
    result = shell.shell("cd --help")

    # Required value
    expected_help = """Command cd.
Give an ability to switch between folders.
Supports 1 flags:
--help
Supports 0 aliases
"""

    # Comparison
    assert result == expected_help


def test_cd_no_parameters_given(fs, setup_fake_environment, reload_cd_module):
    # Call
    shell = Shell()
    result = shell.shell("cd")

    # Comparison
    assert result == ""
    assert constants.CURRENT_DIR == constants.USER_HOME_DIR


def test_cd_to_a_folder(fs, setup_fake_environment, reload_cd_module):
    # Call
    shell = Shell()
    result = shell.shell("cd folder1")

    # Comparison
    assert result == ""
    assert constants.CURRENT_DIR.endswith("folder1")


def test_cd_to_a_nested_folder(fs, setup_fake_environment, reload_cd_module):
    # Call
    shell = Shell()
    result = shell.shell("cd folder1/folder11")

    # Comparison
    assert result == ""
    assert constants.CURRENT_DIR.endswith("folder11")


def test_cd_multiple_times(fs, setup_fake_environment, reload_cd_module):
    # Why not? My console - my rules!
    # Call
    shell = Shell()
    result = shell.shell("cd folder1 folder11")

    # Comparison
    assert result == ""
    assert constants.CURRENT_DIR.endswith("folder11")


def test_cd_invalid_path_error(fs, setup_fake_environment, reload_cd_module):
    # Call
    shell = Shell()
    result = shell.shell("cd nonexistent_folder")

    # Comparison
    assert result == "cd: Path nonexistent_folder doesn't exist!"


def test_cd_to_file_error(fs, setup_fake_environment, reload_cd_module):
    # Call
    shell = Shell()
    result = shell.shell("cd file42")

    # Comparison
    assert result == "cd: You can't switch to file42. It's a file!"
