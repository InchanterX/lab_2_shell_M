from src.shell.shell import Shell


def test_rm_help(fs, setup_fake_environment, reload_cd_module):
    # Call
    shell = Shell()
    result = shell.shell("rm --help")

    # Required value
    expected_help = """Command rm.
Copy files to a different folder.
Supports 2 flags:
--recursive
--force
--help
Supports 2 aliases
-r -f
"""
