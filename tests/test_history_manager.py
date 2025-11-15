from src.infrastructure.history_manager import HistoryManager
import src.infrastructure.constants as constants
import os
import json


def test_history_manager_init(fs, setup_fake_environment):
    # Call
    history = HistoryManager()

    # Comparison
    assert os.path.exists(constants.HISTORY_PATH)
    with open(constants.HISTORY_PATH, "r") as f:
        data = json.load(f)
        assert "meta" in data
        assert "records" in data
        assert data["meta"]["last_reversible_id"] == 0
        assert data["records"] == []


def test_history_manager_record_command(fs, setup_fake_environment):
    # Call
    history = HistoryManager()
    history.record_command("ls", ["all"], ["folder1"], False, None)

    # Comparison
    data = history._read_history()
    assert len(data["records"]) == 1
    assert data["records"][0]["command_name"] == "ls"
    assert data["records"][0]["flag"] == ["all"]
    assert data["records"][0]["parameters"] == ["folder1"]
    assert data["records"][0]["reversible"] is False
    assert data["records"][0]["id"] == 1


def test_history_manager_record_reversible_command(fs, setup_fake_environment):
    # Call
    history = HistoryManager()
    history.record_command("rm", ["force"], ["file1"], True, "/trash/1")

    # Comparison
    data = history._read_history()
    assert len(data["records"]) == 1
    assert data["meta"]["last_reversible_id"] == 1
    assert data["records"][0]["reversible"] is True
    assert data["records"][0]["backup_path"] == "/trash/1"


def test_history_manager_get_last_reversible(fs, setup_fake_environment):
    # Prepare
    history = HistoryManager()
    history.record_command("pwd", [], [], False, None)
    history.record_command("rm", ["force"], ["file1"], True, "/trash/1")
    history.record_command("ls", [], [], False, None)

    # Call
    last_reversible = history.get_last_reversible()

    # Comparison
    assert last_reversible is not None
    assert last_reversible["command_name"] == "rm"
    assert last_reversible["id"] == 2


def test_history_manager_get_last_reversible_none(fs, setup_fake_environment):
    # Prepare
    history = HistoryManager()
    history.record_command("pwd", [], [], False, None)
    history.record_command("ls", [], [], False, None)

    # Call
    last_reversible = history.get_last_reversible()

    # Comparison
    assert last_reversible is None


def test_history_manager_mark_undone(fs, setup_fake_environment):
    # Prepare
    history = HistoryManager()
    history.record_command("rm", ["force"], ["file1"], True, "/trash/1")

    # Call
    history.mark_undone(1)

    # Comparison
    data = history._read_history()
    assert data["records"][0]["undone"] is True


def test_history_manager_get_history_part(fs, setup_fake_environment):
    # Prepare
    history = HistoryManager()
    for i in range(5):
        history.record_command("pwd", [], [], False, None)

    # Call
    part = history.get_history_part(3)

    # Comparison
    assert len(part) == 3
    assert part[0]["id"] == 3
    assert part[1]["id"] == 4
    assert part[2]["id"] == 5


def test_history_manager_get_history_part_exceeding_length(fs, setup_fake_environment):
    # Prepare
    history = HistoryManager()
    for i in range(3):
        history.record_command("pwd", [], [], False, None)

    # Call
    part = history.get_history_part(10)

    # Comparison
    assert len(part) == 3
