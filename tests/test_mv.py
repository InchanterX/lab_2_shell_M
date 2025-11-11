from src.shell.shell import Shell


def test_mv_help(fs, setup_fake_environment, reload_cd_module):
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
