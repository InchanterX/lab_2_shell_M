from src.shell.shell import Shell
import src.infrastructure.constants as constants


def test_pwd_help(fs, setup_fake_environment, reload_pwd_module):
    # Call
    shell = Shell()
    result = shell.shell("pwd --help")

    # Required value
    expected_help = """Command pwd.
Returns current directory.
Supports 1 flags:
--help
Supports 0 aliases
"""

    # Comparison
    assert result == expected_help


def test_pwd_basic_output(fs, setup_fake_environment, reload_pwd_module):
    # Call
    shell = Shell()
    result = shell.shell("pwd")

    # Comparison
    assert result == constants.CURRENT_DIR
