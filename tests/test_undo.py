from src.shell.shell import Shell
import os
import src.infrastructure.constants as constants


def test_undo_help(fs, setup_fake_environment, reload_undo_module):
    # Call
    shell = Shell()
    result = shell.shell("undo --help")

    # Required value
    expected_help = """Command undo.
Undo the last reversible command.
Supports 1 flags:
--help
Supports 0 aliases
"""

    # Comparison
    assert result == expected_help


def test_undo_no_reversible_command(fs, setup_fake_environment, reload_undo_module, reload_ls_module, reload_pwd_module):
    # Prepare
    shell = Shell()
    shell.shell("ls")
    shell.shell("pwd")

    # Call
    result = shell.shell("undo")

    # Comparison
    assert result == "undo: There is no commands to undo."


def test_undo_rm_command(fs, setup_fake_environment, reload_undo_module, reload_rm_module):
    # Prepare
    shell = Shell()
    shell.shell("rm file42")

    # Call
    result = shell.shell("undo")

    # Comparison
    assert "Undid: rm" in result
    assert os.path.exists(os.path.join(constants.CURRENT_DIR, "file42"))


def test_undo_mv_command(fs, setup_fake_environment, reload_undo_module, reload_mv_module):
    # Prepare
    shell = Shell()
    shell.shell("mv file42 folder3")

    # Call
    result = shell.shell("undo")

    # Comparison
    assert "Undid: mv" in result
    assert os.path.exists(os.path.join(constants.CURRENT_DIR, "file42"))
    assert not os.path.exists(os.path.join(
        constants.CURRENT_DIR, "folder3", "file42"))


def test_undo_cp_command(fs, setup_fake_environment, reload_undo_module, reload_cp_module):
    # Prepare
    shell = Shell()
    shell.shell("cp file42 folder3")

    # Call
    result = shell.shell("undo")

    # Comparison
    assert "Undid: cp" in result
    assert not os.path.exists(os.path.join(
        constants.CURRENT_DIR, "folder3", "file42"))


def test_undo_multiple_reversible_commands(fs, setup_fake_environment, reload_undo_module, reload_rm_module, reload_cp_module):
    # Prepare
    shell = Shell()
    shell.shell("rm file42")
    shell.shell("cp folder1/file1 folder3")

    # Call + comparison
    result = shell.shell("undo")
    assert "Undid: cp" in result
    result = shell.shell("undo")
    assert "Undid: rm" in result
    assert os.path.exists(os.path.join(constants.CURRENT_DIR, "file42"))


def test_undo_after_non_reversible_command(fs, setup_fake_environment, reload_undo_module, reload_rm_module, reload_ls_module):
    # Prepare
    shell = Shell()
    shell.shell("rm file42")
    shell.shell("ls")

    # Call
    result = shell.shell("undo")

    # Comparison
    assert "Undid: rm" in result
