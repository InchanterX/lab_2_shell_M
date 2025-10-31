import src.utils.constants as constants
from src.shell.shell import Shell
import logging
import logging.config
from src.common.config import LOGGING_CONFIG


def main() -> None:

    # define logger in accordance with config file
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    logger.info("Logging initialized.")
    print("Console is loading...")

    while True:
        # read users commands
        command = input(f"{constants.USER_LOGIN}|{constants.CURRENT_DIR}>")
        logger.info(f"User entered command: {command}")

        # stop the program if stop word was given
        if command.lower() in ("exit", "quit"):
            print("Exiting the console.")
            break

        # try to process given command
        try:
            shell = Shell()
            result = shell.shell(command)
            if result != "" and result is not None:
                # don't log the result
                print(result)

        # legacy code
        # except OSError:
        #     print("Ошибка операционной системы. Венда удалиться через 3... 2... 1...")

        # return error if it occurred in the program in a pretty way
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
