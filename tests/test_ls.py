import os


def test_ls_current_dir(fs):
    from src.shell.shell import Shell
    shell = Shell()
    result = shell.shell("ls")
    assert "folder1" in result
    assert "folder3" in result
