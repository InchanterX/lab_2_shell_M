from src.infrastructure.tokenizer import Tokenizer
from src.infrastructure.applicator import Applicator
from src.infrastructure.history_manager import HistoryManager
# from src.infrastructure.trash_manager import TrashManager
import logging


class Shell:
    '''
    Gather all the parts of the console and unite them from simpler usage in the future.
    '''

    def __init__(self):
        self._history = HistoryManager()
        # self._trash = TrashManager()
        self._logger = logging.getLogger(__name__)

    def shell(self, command: str) -> str:
        tokens = Tokenizer().tokenize(command)
        applicator = Applicator(tokens)

        command_name = applicator.main_command
        flags = applicator.long_flags
        parameters = applicator.parameters

        result = Applicator(tokens).application()

        reversible = command_name in ("mv", "rm", "cp")
        backup_path = None
        # if reversible:
        #     backup_path = self._trash.create_backup(parameters)

        self._history.record_command(command_name=command_name, flags=flags,
                                     parameters=parameters, reversible=reversible, backup_path=backup_path)
        return result
