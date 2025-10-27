from src.utils.constants import USER_LOGIN, CURRENT_DIR
from src.shell.shell import Shell


def main() -> None:
    print("Console is loading...")

    while True:
        command = input(f"{USER_LOGIN}|{CURRENT_DIR}>")

        if command.lower() in ("exit", "quit"):
            print("Exiting the console.")
            break

        try:
            shell = Shell()
            result = shell.shell(command)
            if result != "" and result != None:
                print(result)
        except OSError:
            print("Ошибка операционной системы. Венда удалиться через 3... 2... 1...")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
