import pytest
from src.utils.tokenizer import Tokenizer, Command_Token


def test_short_flag():
    t = Tokenizer()
    command = "ls -l"
    tokens = t.tokenize(command)
    assert tokens == [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="SHORT_FLAG", value="-l", pos=1)
    ]


def test_long_flag():
    t = Tokenizer()
    command = "ls --long"
    tokens = t.tokenize(command)
    assert tokens == [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="LONG_FLAG", value="--long", pos=1)
    ]


def test_unquoted_windows_path():
    t = Tokenizer()
    command = "ls C:\\folder_name\\file.py"
    tokens = t.tokenize(command)
    assert tokens == [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="UNQUOTED_PARAMETER",
                      value="C:\\folder_name\\file.py", pos=1),
    ]


def test_quoted_windows_path():
    t = Tokenizer()
    command = "ls 'C:\\folder name\\file.py'"
    tokens = t.tokenize(command)
    assert tokens == [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="QUOTED_PARAMETER",
                      value="'C:\\folder name\\file.py'", pos=1),
    ]


def test_unquoted_unix_path():
    t = Tokenizer()
    command = "ls /folder_name/file.py"
    tokens = t.tokenize(command)
    assert tokens == [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="UNQUOTED_PARAMETER",
                      value="/folder_name/file.py", pos=1),
    ]


def test_quoted_unix_path():
    t = Tokenizer()
    command = "ls '/folder name/file.py'"
    tokens = t.tokenize(command)
    assert tokens == [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="QUOTED_PARAMETER",
                      value="'/folder name/file.py'", pos=1),
    ]


def test_not_quoted_path_with_spaces():
    t = Tokenizer()
    command = "ls /folder name/file.py"
    tokens = t.tokenize(command)
    assert tokens == [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="UNQUOTED_PARAMETER", value="/folder", pos=1),
        Command_Token(type="UNQUOTED_PARAMETER", value="name/file.py", pos=2),
    ]


def test_path_and_several_flags():
    t = Tokenizer()
    command = "ls /dir/another_dir/some_file -l -a"
    tokens = t.tokenize(command)
    assert tokens == [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="UNQUOTED_PARAMETER",
                      value="/dir/another_dir/some_file", pos=1),
        Command_Token(type="SHORT_FLAG", value="-l", pos=2),
        Command_Token(type="SHORT_FLAG", value="-a", pos=3),
    ]


def test_several_paths_and_flag():
    t = Tokenizer()
    command = "ls /dir/file1 /dir/subdir/file2 -l"
    tokens = t.tokenize(command)
    assert tokens == [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="UNQUOTED_PARAMETER", value="/dir/file1", pos=1),
        Command_Token(type="UNQUOTED_PARAMETER",
                      value="/dir/subdir/file2", pos=2),
        Command_Token(type="SHORT_FLAG", value="-l", pos=3),
    ]


def test_mixed_flags_and_paths():
    t = Tokenizer()
    command = "ls -l /dir/file1 -a /dir/file2"
    tokens = t.tokenize(command)
    assert tokens == [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="SHORT_FLAG", value="-l", pos=1),
        Command_Token(type="UNQUOTED_PARAMETER", value="/dir/file1", pos=2),
        Command_Token(type="SHORT_FLAG", value="-a", pos=3),
        Command_Token(type="UNQUOTED_PARAMETER", value="/dir/file2", pos=4),
    ]


def test_multiple_spaces():
    t = Tokenizer()
    command = "  ls    -l   /dir/file  "
    tokens = t.tokenize(command)
    assert tokens == [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="SHORT_FLAG", value="-l", pos=1),
        Command_Token(type="UNQUOTED_PARAMETER", value="/dir/file", pos=2),
    ]


def test_several_short_and_long_flags():
    t = Tokenizer()
    command = "ls -lll -l --all --all"
    tokens = t.tokenize(command)
    assert tokens == [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="SHORT_FLAG", value="-lll", pos=1),
        Command_Token(type="SHORT_FLAG", value="-l", pos=2),
        Command_Token(type="LONG_FLAG", value="--all", pos=3),
        Command_Token(type="LONG_FLAG", value="--all", pos=4),
    ]


def test_empty_line():
    t = Tokenizer()
    command = "   "
    tokens = t.tokenize(command)
    assert tokens == []


def test_quoted_parameters():
    t = Tokenizer()
    command = "ls --all 'some file'"
    tokens = t.tokenize(command)
    assert tokens == [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="LONG_FLAG", value="--all", pos=1),
        Command_Token(type="QUOTED_PARAMETER", value="'some file'", pos=2),
    ]


def test_partially_quoted_parameters():
    t = Tokenizer()
    command = "ls --all Desktop/'some file'"
    tokens = t.tokenize(command)
    assert tokens == [
        Command_Token(type="COMMAND", value="ls", pos=0),
        Command_Token(type="LONG_FLAG", value="--all", pos=1),
        Command_Token(type="QUOTED_PARAMETER",
                      value="Desktop/'some file'", pos=2),
    ]


def test_fused_sequence_of_tokens():
    t = Tokenizer()
    command = "/dir/file ls -l"
    with pytest.raises(SyntaxError, match="Command must start with a command name. /dir/file is not a command!"):
        tokens = t.tokenize(command)


def test_fused_sequence_of_tokens():
    t = Tokenizer()
    command = "ls &"
    with pytest.raises(SyntaxError, match="Invalid value & on position 1!"):
        tokens = t.tokenize(command)
