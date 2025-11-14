import logging
from src.services.help_call import Helper
from src.infrastructure.history_manager import HistoryManager


class History:
    '''
    "History returns last N elements of .history. Returns 10 by default."
    '''

    def __init__(self, helper: Helper, history_manager: HistoryManager) -> None:
        self._helper = helper
        self._history_manager = history_manager
        self._logger = logging.getLogger(__name__)

    def history(self, long_flags: list[str], parameters: list[str]) -> str:
        self._logger.debug(
            f"Running history with flags={long_flags}, parameters={parameters}")

        # help call
        if 'help' in long_flags:
            return self._helper.call_help("history")

        # determine how many records to show
        n = 10
        output = []
        if len(parameters) == 1:
            try:
                n = int(parameters[0])
                if n < 1:
                    n = 10
            except ValueError:
                self._logger.warning(
                    f"Invalid number parameter {parameters[0]}.")
                output.append(
                    f"Parameter {parameters[0]} is invalid! Returns last 10 history elements.")
                n = 10

        # get N history elements
        records = self._history_manager.get_history_part(n)

        # if history is empty
        if not records:
            return "No commands in history."

        # processing history elements
        for record in records:
            command_name = record["command_name"]
            if record["flag"]:
                flags_str = " ".join(f"--{flag}" for flag in record["flag"])
                command_name += f" {flags_str}"
            if record["parameters"]:
                params_str = " ".join(record["parameters"])
                command_name += f" {params_str}"

            status = " (undone)" if record["undone"] else ""
            output.append(f"{record['id']}: {command_name}{status}")

        return "\n".join(output)


COMMAND_INFO = {
    "name": "history",
    "function": lambda: History(Helper(), HistoryManager()),
    "entry-point": "history",
    "flags": ["help"],
    "aliases": {},
    "description": "Display command history."
}
