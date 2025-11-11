from src.shell.shell import Shell


def test_zip_help(fs, setup_fake_environment, reload_cd_module):
    # Call
    shell = Shell()
    result = shell.shell("zip --help")

    # Required value
    expected_help = """Command zip.
Zip given files.
Supports 1 flags:
--help
Supports 0 aliases
"""

    # Comparison
    assert result == expected_help
