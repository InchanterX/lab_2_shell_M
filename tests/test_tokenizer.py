import pytest
from src.utils.tokenizer import Tokenizer, Command_Token


@pytest.mark.parametrize("command, expected_output", [
    # short flag
    ("ls -l", [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="SHORT_FLAG", value="-l", pos=1),
    ]),

    # long flag
    ("ls --help", [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="LONG_FLAG", value="--help", pos=1),
    ]),

    # unquoted Windows paths
    ("ls C:\\folder_name\\file.py", [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="UNQUOTED_PARAMETER",
                      value="C:\\folder_name\\file.py", pos=1),
    ]),

    # quoted Windows paths
    ("ls 'C:\\folder name\\file.py'", [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="QUOTED_PARAMETER",
                      value="'C:\\folder name\\file.py'", pos=1),
    ]),

    # unquoted Unix path
    ("ls /folder_name/file.py", [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="UNQUOTED_PARAMETER",
                      value="/folder_name/file.py", pos=1),
    ]),

    # quoted Unix path
    ("ls '/folder name/file.py'", [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="QUOTED_PARAMETER",
                      value="'/folder name/file.py'", pos=1),
    ]),

    # not quoted path
    ("ls /folder name/file.py", [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="UNQUOTED_PARAMETER", value="/folder", pos=1),
        Command_Token(type="UNQUOTED_PARAMETER", value="name/file.py", pos=2),
    ]),

    # path and several flags
    ("ls /dir/another_dir/some_file -l -a", [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="UNQUOTED_PARAMETER",
                      value="/dir/another_dir/some_file", pos=1),
        Command_Token(type="SHORT_FLAG", value="-l", pos=2),
        Command_Token(type="SHORT_FLAG", value="-a", pos=3),
    ]),

    # several paths and flag
    ("ls /dir/file1 /dir/subdir/file2 -l", [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="UNQUOTED_PARAMETER", value="/dir/file1", pos=1),
        Command_Token(type="UNQUOTED_PARAMETER",
                      value="/dir/subdir/file2", pos=2),
        Command_Token(type="SHORT_FLAG", value="-l", pos=3),
    ]),

    # mixed flags and paths
    ("ls -l /dir/file1 -a /dir/file2", [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="SHORT_FLAG", value="-l", pos=1),
        Command_Token(type="UNQUOTED_PARAMETER", value="/dir/file1", pos=2),
        Command_Token(type="SHORT_FLAG", value="-a", pos=3),
        Command_Token(type="UNQUOTED_PARAMETER", value="/dir/file2", pos=4),
    ]),

    # multiple spaces
    ("  ls    -l   /dir/file  ", [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="SHORT_FLAG", value="-l", pos=1),
        Command_Token(type="UNQUOTED_PARAMETER", value="/dir/file", pos=2),
    ]),

    # fused sequence of tokens
    ("/dir/file ls -l", [
        Command_Token(type="UNQUOTED_PARAMETER", value="/dir/file", pos=0),
        Command_Token(type="COMMAND", value="ls", pos=1),
        Command_Token(type="SHORT_FLAG", value="-l", pos=2),
    ]),

    # several sort and long flags
    ("ls -lll -l --all --all", [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="SHORT_FLAG", value="-lll", pos=1),
        Command_Token(type="SHORT_FLAG", value="-l", pos=2),
        Command_Token(type="LONG_FLAG", value="--all", pos=3),
        Command_Token(type="LONG_FLAG", value="--all", pos=4),
    ]),

    # empty line
    ("   ", []),
])
def test_tokenizer_valid_commands(command, expected_output):
    assert Tokenizer().tokenize(command) == expected_output
