import src.utils.constants as constants
from src.shell.shell import Shell
import logging
import logging.config
from src.common.config import LOGGING_CONFIG


def main() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    logger.info("Logging initialized.")
    print("Console is loading...")

    while True:
        command = input(f"{constants.USER_LOGIN}|{constants.CURRENT_DIR}>")

        if command.lower() in ("exit", "quit"):
            print("Exiting the console.")
            break

        try:
            shell = Shell()
            result = shell.shell(command)
            if result != "" and result != None:
                print(result)
        # except OSError:
        #     print("Ошибка операционной системы. Венда удалиться через 3... 2... 1...")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
