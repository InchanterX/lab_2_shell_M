from src.shell.shell import Shell


def test_untar_help(fs, setup_fake_environment, reload_cd_module):
    # Call
    shell = Shell()
    result = shell.shell("untar --help")

    # Required value
    expected_help = """Command untar.
Untar zip archives.
Supports 1 flags:
--help
Supports 0 aliases
"""

    # Comparison
    assert result == expected_help
