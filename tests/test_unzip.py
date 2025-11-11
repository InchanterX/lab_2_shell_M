from src.shell.shell import Shell


def test_unzip_help(fs, setup_fake_environment, reload_cd_module):
    # Call
    shell = Shell()
    result = shell.shell("unzip --help")

    # Required value
    expected_help = """Command unzip.
Unzip zip archives.
Supports 1 flags:
--help
Supports 0 aliases
"""

    # Comparison
    assert result == expected_help
