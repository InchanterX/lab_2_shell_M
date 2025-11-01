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
    │                ├── archive.py            # archives files
    │                ├── basic_cat.py          # displays files content
    │                ├── basic_cd.py           # changes current directory
    │                ├── basic_cp.py           # copies files
    │                ├── basic_ls.py           # lists files
    │                ├── basic_mv.py           # moves files
    │                ├── basic_rm.py           # deletes files
    │                ├── grep.py               # searches matches
    │                ├── history.py            # saves and lists user actions
    │                ├── undo.py               # reverses users actions
    │            ├──user_commands              # commands added by users
    │                ├── example.py            # command example for users
    │            ├── __init__.py               #
    │       ├── shell/                         # project building folder
    │            ├── __init__.py               #
    │            ├── shell.py                  # gather all classes in one for a simpler usage
    │       ├── utils/                         # console building utilities
    │            ├── __init__.py               #
    │            ├── applicator.py             # applies command to tokens
    │            ├── colorizer.py              # prepares colors for commands colorizing
    │            ├── constants.py              # contains constants and regular expressions
    │            ├── path_normalizer.py        # converts paths to a standard
    │            ├── registry.py               # registers commands
    │            ├── tokenizer.py              # converts commands into tokens
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