It's a Shell level M project with a terminal that dynamically load all given commands to registry.

# Project structure

 <pre>
    .
    ├── lab_2_shell_m
    │   ├── .trash                             # Store deleted files
    │   ├── .shell_log                         # Source code
    │       ├── shell.log                      # log file
    │   ├── src/                               # Source code
    │       ├── common/                        # config files
    │            ├──__init__.py                #
    │            ├──config.py                  # logger configuration
    │       ├── core/                          # terminal commands
    │            ├──commands                   # system commands required by TT
    │                ├── __init__.py           #
    │                ├── basic_cat.py          # displays files content
    │                ├── basic_cd.py           # changes current directory
    │                ├── basic_cp.py           # copies files
    │                ├── basic_ls.py           # lists files
    │                ├── basic_mv.py           # moves files
    │                ├── basic_rm.py           # deletes files
    │                ├── grep.py               # searches matches
    │                ├── history.py            # lists user actions
    │                ├── tar.py                # converts files to a .tar files
    │                ├── undo.py               # reverses users actions
    │                ├── untar.py              # untars .tar files
    │                ├── unzip.py              # unzips .zip files
    │                ├── zip.py                # converts files to a .zip files
    │            ├──user_commands              # commands added by users
    │                ├── example.py            # command example for users
    │                ├── pwd.py                # shows current directory
    │            ├── __init__.py               #
    │       ├── infrastructure/                # main functions of the console
    │            ├── __init__.py               #
    │            ├── applicator.py             # applies command to tokens
    │            ├── colorizer.py              # prepares colors for commands colorizing
    │            ├── constants.py              # contains constants and regular expressions
    │            ├── registry.py               # registers commands
    │            ├── tokenizer.py              # converts commands into tokens
    │            ├── history_manager.py        # save history of used commands to .history
    │            ├── trash_manager.py          # make backups of commands that can be undone
    │       ├── shell/                         # project building folder
    │            ├── __init__.py               #
    │            ├── shell.py                  # gather all classes in one for a simpler usage
    |       ├── services/                      # common functions for usage in commands
    │            ├── __init__.py               #
    │            ├── help_call.py              # shows information about the command
    │            ├── path_normalizer.py        # converts paths to a standard form
    |       ├── __init__.py                    #
    |       ├── main.py                        # It's a main file!
    │   ├── tests/                             # Unit tests
    │       ├── test_tokenizer.py              # Test commands tokenization
    │       ├── test_basic_cat.py              # Test command cat
    │   ├── .gitignore                         # git ignore files
    │   ├── .pre-commit-config.yaml            # Code-style check
    │   ├── .history/                          # History folder
    │       ├── history.json                   # JSON file with commands history
    │   ├── pyproject.toml                     # Project configuration
    │   ├── requirements.txt                   # Dependencies
    │   ├── README.md                          # Laboratory report with a project description
</pre>

# Set up
To use this "shell" you need to download it. Then you can run it from the project root with your terminal with:
```
python -m src.main
```

## Tests
To ran tests you need to have pytest, pytest-pyfakefs, pytest-cov.
To activate tests use:
```
python -m pytest
```

# How it works?
Program is cross-platform (works on Windows|UNIX) is split in 2 logical parts: console and commands.
- Console runs CLI, process all the commands that exists and processes users input.
- Commands are stored in a separate folders and also split by 2 parts: initial commands (standard pack) and commands made by users.

## Registry
Registry create a registry of all available commands from src/core folder by dynamically importing and analyzing config variables in them. As a result it generates dictionary of all valid commands.

## Constants
Constants file contains variables of constant values: base directory, lists of commands, flags, parts of the regular expressions for tokenization and master regular expression.

## Tokenizer
Tokenizer process result of master's regular expression and put them to a list. Every token is stored in form of data class.

## Applicator
Applicator normalize commands flags, prepare class and function for command call by finding them in registry. Returns command work result.

## History Manager
Get tokens, create history elements and add them to the file .history/history.json in the project root. Command distinguish which commands can be undone or not.

## Trash manager
Make backups of files that will be changed by cp/mv/rm commands work in folder .trash. Also provide an ability to restore files from trash back.

## Shell
Shell file serves the purpose of building a solid file to easily call input command processing. Make a consistent calls of infrastructure classes.

## Main
Main file starts the terminal and returns result of Shell() work.

# Services
Folder contains all files with general functions can be used in commands (both used in basic commands and can be used in user's commands)

## Help Call
Returns informational message to the console about the asked command. Builds it's input based on information stored in the command configuration and therefore in registry.

## Path Normalizer
Convert given path to an absolute normalized unfolded and unquoted version of it and returns original and processed path.

# Embedded commands
Standard library of commands provided with console.
Every command contains configuration variable that stores command name, class with all the used services, main function name, available flags, their shortenings and descriptions.

## Cd
Command allow user to change current directory that is stored in the constant.

## Cat
Command print content of a file if it is not a folder or not a binary file. If an exception ocurred adds information to the output.

## Cp
Command copy files and directories to a target folder. Folders with content in them can be copied only with --recursive flag.

## Ls
Command lists given folders. Supports showing hidden files using flag --all and showing wider list of information about every file via flag --long.

## Mv
Command that move file to a target place. If only two files were given it will work as a renaming. But in basic cases all the files will be moved to a target folder if everything is valid.

## Rm
Command removes given files. Files can always be easily removed. Folders can be deleted with user confirmation or --recursive flags. Or you can just --force everything and ignore all unpleasant questions.

## Archive (zip, unzip, tar, untar)
These 2 pairs of commands are used to work with archives. You can gather files to 2 types of archives using zip and tar. And unzip them by unzip and untar. New archives appears in the current folder with a name "archive$.\[zip|tar.gz]" where $ is a number that prevents files collisions.

## Grep
Search by regular expression from the command parameter in the given parameters. Returns list of all matches in every file with line number. Supports flag -r and -i. -r allow user to search in folders. -i allow user to ignore letters cases.

## History
Returns last N elements of .history/history.json file depending on the entered parameter. Returns 10 elements  by default. If N exceeds current history len it will be rounded to the length of the history.

## Undo
Using functions of history manager and trash manager to find the command that should be undone in .history/history.json and if there is no errors restores it from .trash.

# Users commands
Users of the console can do their own commands and easily add them to the other commands using services and basic structure.
In folder src/core/user_commands you can find an example of user's command and write your own the same way.

## Small guide about making pwd by your own
1. First of all, you need to make a python file with a name you like. For pwd it will be "pwd.py".
2. Then you need to make this file a command at point of view of the console by adding a configuration variable.
Fields of flags, aliases and descriptions are not mandatory and can be empty ({} or "")
```python
COMMAND_INFO = {
    "name": "pwd", # command name
    "function": lambda: Pwd(Helper()), # factory with command class and services that are used in command
    "entry-point": "pwd", # main function that runs the command
    "flags": ["help"], # flags that can be applied to you command
    "aliases": {"h": "help"}, # shortenings to you flags
    "description": "Returns current directory." # Just a description
}
```
3. Build basic structure of your command as it made in example
```python
class Pwd:
    '''
    Command "pwd" returns current directory
    '''

    def __init__(self) -> None: # im
        ...

    def pwd(self, long_flags: list[str], parameters: list[str]) -> str: # input is basic for all the commands
        ...
```
4. Add services that you would like to use in your code:
```python
import src.infrastructure.constants as constants # you can easily access basic vars through constants
from src.infrastructure.logger import logger # logger call
from src.services.help_call import Helper # all services are stored in src.services


class Pwd:
    '''
    Command "pwd" returns current directory
    '''

    def __init__(self, helper: Helper) -> None: # add services you want
        self._helper = helper # and add them here
        self._logger = logger

    def pwd(self, long_flags: list[str], parameters: list[str]) -> str: # input is basic for all the commands
        ...
```

1. And now you can create whatever you want! After finishing all you need to do is to save your file and on the next launch of the console it will appear. Here is the example of ready pwd command.
```python
from src.infrastructure.logger import logger
import src.infrastructure.constants as constants
from src.services.help_call import Helper


class Pwd:
    '''
    Command "pwd" returns current directory
    '''

    def __init__(self, helper: Helper) -> None:
        self._helper = helper
        self._logger = logger

    def pwd(self, long_flags: list[str], parameters: list[str]) -> str:
        self._logger.debug(
            f"Running pwd with flags={long_flags}, parameters={parameters}")

        # help call
        if 'help' in long_flags:
            return self._helper.call_help("pwd")

        return constants.CURRENT_DIR


COMMAND_INFO = {
    "name": "pwd",
    "function": lambda: Pwd(Helper()),
    "entry-point": "pwd",
    "flags": ["help"],
    "aliases": {},
    "description": "Returns current directory."
}

```

## Making tests for user's commands
If you are really despaired about making tests for your own commands, you can also do it quite easy by following this steps:
1. You need to define your command for testing in "tests/conftest.py" file by adding a fixture, adding the name of you command that you put to the parameter "name" in the command config.
```python
@pytest.fixture
def reload_NAME_module():
    '''Fixture to reload NAME module.'''
    return _reload_command_module("NAME")
```
2. Create a file for your tests in folder "tests/"
3. That's it. You can write your tests: import libraries that you need, use prepared fake system from conftest to work with files.
```python
# importing all the things you need
# there is no need to import conftest
from src.shell.shell import Shell
import src.infrastructure.constants as constants

# test for help call
def test_pwd_help(fs, setup_fake_environment, reload_pwd_module):
    # Call
    shell = Shell()
    result = shell.shell("pwd --help")

    # Required value
    expected_help = """Command pwd.
Returns current directory.
Supports 1 flags:
--help
Supports 0 aliases
"""

    # Comparison
    assert result == expected_help

# test for commands' basic functional
def test_pwd_basic_output(fs, setup_fake_environment, reload_pwd_module):
    # Call
    shell = Shell()
    result = shell.shell("pwd")

    # Comparison
    assert result == constants.CURRENT_DIR
```
