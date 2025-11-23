import src.infrastructure.constants as constants
from src.shell.shell import Shell
import logging.config
from src.common.config import LOGGING_CONFIG
from src.infrastructure.logger import logger


def main() -> None:

    # define logger in accordance with config file
    logging.config.dictConfig(LOGGING_CONFIG)
    # logger = logging.getLogger(__name__)
    logger.info("Logging initialized.")
    print("Console is loading...")

    try:
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

            # catch unexpected os errors
            except OSError as e:
                logger.exception(
                    f"Command failed to execute with a error: {e}")
                print("An unexpected os error occurred. Check log file for information.")
    except KeyboardInterrupt:
        print("Exiting the console.")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
