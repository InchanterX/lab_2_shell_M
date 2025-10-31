import os
import re
from src.utils.registry import Registry

# Define basic paths
USER_HOME_DIR = os.path.expanduser("~")
USER_LOGIN = os.getlogin()
CURRENT_DIR = USER_HOME_DIR
LOG_DIR = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "../../.shell_log")

# Modules data
SUCCESS, REGISTRY = Registry().registration()
NAMES = list(REGISTRY.keys())
FLAGS = set(flag for name in NAMES for flag in REGISTRY[name]["flags"])

# Regular expression for spaces
PURE_SPACE_RE = r"(\s+)"
SPACE_RE = f"(?P<SPACE>{PURE_SPACE_RE})"

# Regular expression for commands
PURE_COMMANDS_RE = f"({'|'.join(re.escape(name) for name in NAMES)})"
COMMANDS_RE = f"(?P<COMMAND>{PURE_COMMANDS_RE})"

# Regular expression for flags
SHORT_FLAGS = [flag for flag in FLAGS if len(flag) == 1]
LONG_FLAGS = [flag for flag in FLAGS if len(flag) > 1]
PURE_SHORT_FLAGS_RE = "-[a-zA-Z]+"
PURE_LONG_FLAGS_RE = "--[a-zA-Z-]+"
SHORT_FLAGS_RE = f"(?P<SHORT_FLAG>{PURE_SHORT_FLAGS_RE})"
LONG_FLAGS_RE = f"(?P<LONG_FLAG>{PURE_LONG_FLAGS_RE})"

# Regular expression for parameters
PURE_UNQUOTED_PARAMETERS_RE = r"[a-zA-Zа-яА-ЯёЁ0-9_\-./\\~\(\):]+"
PURE_QUOTED_PARAMETERS_RE = r"'([^']*)'|\"([^\"]*)\""
UNQUOTED_PARAMETERS_RE = f"(?P<UNQUOTED_PARAMETER>{PURE_UNQUOTED_PARAMETERS_RE})"
QUOTED_PARAMETERS_RE = f"(?P<QUOTED_PARAMETER>{PURE_QUOTED_PARAMETERS_RE})"

# Regular expression for all that remained
UNKNOWN_RE = "(?P<UNKNOWN>.)"

# Ordered regular expressions
ALL_EXPRESSIONS = [COMMANDS_RE, LONG_FLAGS_RE, SHORT_FLAGS_RE,
                   QUOTED_PARAMETERS_RE, UNQUOTED_PARAMETERS_RE, SPACE_RE, UNKNOWN_RE]

# Master regular expression to gather all in one
MASTER_RE = re.compile('|'.join(ALL_EXPRESSIONS))
