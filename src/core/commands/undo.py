import logging
from src.services.help_call import Helper
from src.infrastructure.history_manager import HistoryManager
from src.infrastructure.trash_manager import TrashManager


class Undo:
    '''
    "undo" undo the last reversible command: rm, mv, or cp, using history and trash managers.
    '''

    def __init__(self, helper: Helper, history_manager: HistoryManager, trash_manager: TrashManager) -> None:
        self._helper = helper
        self._history_manager = history_manager
        self._trash_manager = trash_manager
        self._logger = logging.getLogger(__name__)

    def undo(self, long_flags: list[str], parameters: list[str]) -> str:
        self._logger.debug(
            f"Running undo with flags={long_flags}, parameters={parameters}")

        # help call
        if 'help' in long_flags:
            return self._helper.call_help("undo")

        # get last reversible command
        last_reversible = self._history_manager.get_last_reversible()

        if last_reversible is None:
            return "undo: There is no commands to undo."

        command_name = last_reversible["command_name"]
        command_id = last_reversible["id"]
        command_params = last_reversible["parameters"]

        # restore
        success = self._trash_manager.restore_backup(
            command_id, command_name, command_params)

        if success:
            # mark command as undone
            self._history_manager.mark_undone(command_id)

            # update last_reversible_id to previous reversible command
            history = self._history_manager._read_history()
            records = history["records"]
            previous_reversible_id = 0
            for record in reversed(records):
                if record["reversible"] and record["id"] < command_id and not record["undone"]:
                    previous_reversible_id = record["id"]
                    break

            history["meta"]["last_reversible_id"] = previous_reversible_id
            self._history_manager._write_history(history)

            self._logger.info(f"Undid command {command_id} {command_name}")
            return f"Undid: {command_name} {' '.join(command_params)}"
        else:
            return f"undo: Failed to restore command {command_id} from the backup."


COMMAND_INFO = {
    "name": "undo",
    "function": lambda: Undo(Helper(), HistoryManager(), TrashManager()),
    "entry-point": "undo",
    "flags": ["help"],
    "aliases": {},
    "description": "Undo the last reversible command."
}
