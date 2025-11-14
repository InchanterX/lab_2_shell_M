from src.shell.shell import Shell


def test_history_help(fs, setup_fake_environment, reload_history_module):
    # Call
    shell = Shell()
    result = shell.shell("history --help")

    # Required value
    expected_help = """Command history.
Display command history.
Supports 1 flags:
--help
Supports 0 aliases
"""

    # Comparison
    assert result == expected_help


def test_history_empty_history(fs, setup_fake_environment, reload_history_module):
    # Call
    shell = Shell()
    result = shell.shell("history")

    # Comparison
    assert result == "No commands in history."


def test_history_show_last_commands(fs, setup_fake_environment, reload_history_module, reload_ls_module, reload_pwd_module, reload_cat_module):
    # Prepare
    shell = Shell()
    shell.shell("ls")
    shell.shell("pwd")
    shell.shell("cat file42")

    # Call
    result = shell.shell("history")

    # Comparison
    assert "1:" in result
    assert "2:" in result
    assert "3:" in result
    assert "ls" in result
    assert "pwd" in result
    assert "cat" in result


def test_history_show_specific_number(fs, setup_fake_environment, reload_history_module, reload_pwd_module):
    # Prepare
    shell = Shell()
    for i in range(5):
        shell.shell("pwd")

    # Call
    result = shell.shell("history 3")

    # Comparison
    lines = result.split("\n")
    assert len(lines) == 3
    assert "3:" in result
    assert "4:" in result
    assert "5:" in result


def test_history_show_undone_command(fs, setup_fake_environment, reload_history_module, reload_undo_module, reload_rm_module):
    # Prepare
    shell = Shell()
    shell.shell("rm file42")
    shell.shell("undo")

    # Call
    result = shell.shell("history")

    # Comparison
    assert "(undone)" in result


def test_history_invalid_number_parameter(fs, setup_fake_environment, reload_history_module, reload_pwd_module):
    # Prepare
    shell = Shell()
    shell.shell("pwd")

    # Call
    result = shell.shell("history poop")

    # Comparison
    assert "1:" in result
