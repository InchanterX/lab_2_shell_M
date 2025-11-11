from src.shell.shell import Shell


def test_tar_help(fs, setup_fake_environment, reload_cd_module):
    # Call
    shell = Shell()
    result = shell.shell("tar --help")

    # Required value
    expected_help = """Command tar.
Tar given files.
Supports 1 flags:
--help
Supports 0 aliases
"""

    # Comparison
    assert result == expected_help
