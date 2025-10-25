import pytest
from src.utils.tokenizer import Tokenizer


@pytest.mark.parametrize("command, expected_output", [
    ("ls -l", ),
    ("ls --help", )
])
def test_tokenizer_valid_commands(command, expected_output):
    assert Tokenizer().tokenize(command) == expected_output
