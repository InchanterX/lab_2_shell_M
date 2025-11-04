from src.infrastructure.tokenizer import Tokenizer
from src.infrastructure.applicator import Applicator


class Shell:
    '''
    Gather all the parts of the console and unite them from simpler usage in the future.
    '''

    def shell(self, command: str) -> str:
        tokens = Tokenizer().tokenize(command)
        result = Applicator(tokens).application()
        return result
