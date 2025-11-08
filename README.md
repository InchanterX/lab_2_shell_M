It's a Shell level M project with a terminal that dynamically load all given commands to registry.

# Project structure

 <pre>
    .
    ├── lab_2_shell_m
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
    │                ├── history.py            # saves and lists user actions
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
    │   ├── pyproject.toml                     # Project configuration
    │   ├── requirements.txt                   # Dependencies
    │   ├── README.md                          # Laboratory report with a project description
</pre>

# Set up
To use calculator you need to download it. Then you can run it from the project root with your terminal with:
```
python -m src.main
```
To activate tests use:
```
python -m pytest
```

# How it works?
Program is split in 2 logical parts: console and commands.
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

##