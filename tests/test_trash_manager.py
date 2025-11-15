from src.infrastructure.trash_manager import TrashManager
import src.infrastructure.constants as constants
import os


def test_trash_manager_init(fs, setup_fake_environment):
    # Call
    trash = TrashManager()

    # Comparison
    assert os.path.exists(constants.TRASH_DIR)


def test_trash_manager_prohibited_paths_return(fs, setup_fake_environment):
    # Call
    trash = TrashManager()

    # Test case of Unix root
    assert trash._is_prohibited_path("/") is True

    # Test case of Windows root
    if os.name == "nt":
        assert trash._is_prohibited_path("C:\\") is True
        assert trash._is_prohibited_path("C:") is True

    # Base case
    assert trash._is_prohibited_path("/home/user/file.txt") is False
    assert trash._is_prohibited_path("file.txt") is False


def test_trash_manager_create_backup_rm(fs, setup_fake_environment):
    # Call
    trash = TrashManager()

    # Prepare
    test_file = "test_backup.txt"
    fs.create_file(f"{constants.CURRENT_DIR}/{test_file}",
                   contents="test content")

    # One More Call
    backup_path = trash.create_backup(1, "rm", [test_file])

    # Comparison
    assert backup_path is not None
    assert os.path.exists(backup_path)
    assert os.path.exists(os.path.join(backup_path, "test_backup.txt"))


def test_trash_manager_create_backup_skiping_prohibited_paths(fs, setup_fake_environment):
    # Call
    trash = TrashManager()

    # Prepare
    backup_path = trash.create_backup(1, "rm", ["/"])

    # Comparison
    assert backup_path is None


# def test_trash_manager_restore_backup_rm(fs, setup_fake_environment):
#     # Call
#     trash = TrashManager()

#     # Prepare
#     test_file = "test_restore.txt"
#     full_path = f"{constants.CURRENT_DIR}/{test_file}"
#     fs.create_file(full_path, contents="original content")
#     # backup_path = trash.create_backup(1, "rm", [test_file])
#     os.remove(full_path)
#     assert not os.path.exists(full_path)

#     # Call
#     result = trash.restore_backup(1, "rm", [test_file])

#     # Comparison
#     assert result is True
#     assert os.path.exists(full_path)
#     with open(full_path, "r") as f:
#         assert f.read() == "original content"
