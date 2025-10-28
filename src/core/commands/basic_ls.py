import os
import stat
import datetime
import src.utils.constants as constants


class Ls:
    '''
    Command "list"
    '''

    def __init__(self) -> None:
        pass

    def ls(self, long_flags: list[str], parameters: list[str]) -> str:
        if 'help' in long_flags:
            return 'ls lists folders'
        results = []
        output = []
        dirs = []
        if parameters == []:
            results.append(os.listdir(constants.CURRENT_DIR))
            parameters.append(constants.CURRENT_DIR)
            dirs.append(constants.CURRENT_DIR)
        else:
            for parameter in parameters:
                original_parameter = parameter
                parameter = os.path.expanduser(parameter)
                if not os.path.isabs(parameter):
                    parameter = os.path.join(constants.CURRENT_DIR, parameter)
                parameter = os.path.normpath(parameter)
                if os.path.isfile(parameter):
                    # error here
                    output.append([
                        f"ls: {original_parameter} can't be listed. It's a file!"])
                elif os.path.isdir(parameter):
                    results.append(os.listdir(parameter))
                    dirs.append(parameter)
                else:
                    # error here
                    output.append([
                        f"ls: Path {original_parameter} is invalid!"])

        if 'all' not in long_flags:
            for r in range(len(results)):
                results[r] = [file for file in results[r]
                              if not file.startswith('.')]
        if 'long' in long_flags:
            for r in range(len(results)):
                for file in results[r]:
                    file_stat = os.stat(os.path.join(dirs[r], file))
                    if os.name == 'nt':
                        # date = datetime.datetime.fromtimestamp(
                        #     file_stat.st_mtime)
                        print(stat.filemode(file_stat.st_mode),
                              file_stat.st_nlink, "owner", "group", file_stat.st_size, datetime.datetime.fromtimestamp(
                            file_stat.st_mtime).strftime("%b %d %H:%M"), file)
                    else:
                        # output with uid git for Linux

        return results


COMMAND_INFO = {
    "name": "ls",
    "function": Ls,
    "entry-point": "ls",
    "flags": ["all", "long", "human-readable", "help"],
    "aliases": {"a": "all", "l": "long", "h": "human-readable"},
    "description": "List files in the given folder."


}
