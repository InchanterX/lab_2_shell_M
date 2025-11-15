import json
import os
import datetime
import src.infrastructure.constants as constants


class HistoryManager:
    '''
    "HistoryManager" manages commands history by saving them a separated JSON file.
    It separately stores if command can be undone or not and provide possibility to find last command that can be undone with O(1).
    '''

    def __init__(self) -> None:
        if not os.path.exists(constants.HISTORY_PATH):
            os.makedirs(os.path.dirname(constants.HISTORY_PATH), exist_ok=True)
            with open(constants.HISTORY_PATH, "w", encoding="UTF-8") as file:
                json.dump({"meta": {"last_reversible_id": 0},
                          "records": []}, file, indent=2)

    def _read_history(self) -> dict:
        with open(constants.HISTORY_PATH, "r", encoding="UTF-8") as file:
            return json.load(file)

    def _write_history(self, new_elements: dict):
        with open(constants.HISTORY_PATH, "w", encoding="UTF-8") as file:
            return json.dump(new_elements, file, indent=2)

    def record_command(self, command_name: str, flags: list[str], parameters: list[str], reversible: bool, backup_path: str) -> None:
        history = self._read_history()
        next_id = len(history["records"]) + 1
        records = history["records"]
        last_reversible_id = (
            next_id if reversible else history["meta"]["last_reversible_id"])

        new_history_record = {"id": next_id,
                              "time": datetime.datetime.now().isoformat(),
                              "command_name": command_name,
                              "flag": flags,
                              "parameters": parameters,
                              "reversible": reversible,
                              "last_reversible_id": last_reversible_id,
                              "backup_path": backup_path,
                              "undone": False
                              }

        records.append(new_history_record)
        if reversible:
            history["meta"]["last_reversible_id"] = next_id
        self._write_history(history)

    def get_last_reversible(self) -> dict | None:
        '''
        Return last command that can be undone. Or None if there is no commands to undone.
        '''
        history = self._read_history()
        last_id = history["meta"]["last_reversible_id"]
        if last_id == 0:
            return None

        for line in reversed(history["records"]):
            if line["id"] == last_id and not line["undone"]:
                return line
        return None

    def mark_undone(self, id: int) -> None:
        '''
        Mark a command as undone.
        '''
        history = self._read_history()
        for line in history["records"]:
            if line["id"] == id:
                line["undone"] = True
                break
        self._write_history(history)

    def get_history_part(self, n: int = 10) -> list[dict]:
        '''
        Returns last N elements of history.
        Or all elements if N is bigger than history size.
        '''
        history = self._read_history()
        records = history["records"]
        return records[-n:] if len(records) > n else records
