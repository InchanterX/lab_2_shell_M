from src.infrastructure.tokenizer import Tokenizer
from src.infrastructure.applicator import Applicator
from src.infrastructure.history_manager import HistoryManager
from src.infrastructure.trash_manager import TrashManager
from src.infrastructure.logger import logger


class Shell:
    '''
    Gathers all the parts of the console and unite them from simpler usage in the future.
    '''

    def __init__(self):
        self._history = HistoryManager()
        self._trash = TrashManager()
        self._logger = logger

    def shell(self, command: str) -> str:
        tokens = Tokenizer().tokenize(command)
        applicator = Applicator(tokens)

        command_name = applicator.main_command
        flags = applicator.long_flags
        parameters = applicator.parameters

        # Check if command can be undone a create a backup in .trash for it
        reversible = command_name in ("mv", "rm", "cp")
        backup_path = None

        if reversible:
            history = self._history._read_history()
            next_id = len(history["records"]) + 1
            backup_path = self._trash.create_backup(
                next_id, command_name, parameters)

        # Execute command
        result = Applicator(tokens).application()

        # Record command to the .history
        self._history.record_command(
            command_name=command_name,
            flags=flags,
            parameters=parameters,
            reversible=reversible,
            backup_path=backup_path
        )
        return result
