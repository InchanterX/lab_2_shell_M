import os
import re
# import pprint
from src.utils.registry import Registry

USER_HOME_DIR = os.path.expanduser("~")

# Modules data
REGISTRY = Registry().registration()
NAMES = list(REGISTRY.keys())
FLAGS = set(flag for name in NAMES for flag in REGISTRY[name]["flags"])

# pprint.pprint(REGISTRY)

# Regular expression for spaces
PURE_SPACE_RE = r"(\s+)"
SPACE_RE = f"(?P<SPACE>{PURE_SPACE_RE})"

# Regular expression for commands
PURE_COMMANDS_RE = f"({'|'.join(re.escape(name) for name in NAMES)})"
COMMANDS_RE = f"(?P<COMMAND>{PURE_COMMANDS_RE})"

# Regular expression for flags
SHORT_FLAGS = [flag for flag in FLAGS if len(flag) == 1]
LONG_FLAGS = [flag for flag in FLAGS if len(flag) > 1]
# PURE_SHORT_FLAGS_RE = f"-[{''.join(re.escape(short_flag) for short_flag in SHORT_FLAGS)}]+"
PURE_SHORT_FLAGS_RE = f"-[a-zA-Z]+"
# PURE_LONG_FLAGS_RE = f"--({'|'.join(re.escape(long_flag) for long_flag in LONG_FLAGS)})"
PURE_LONG_FLAGS_RE = f"--[a-zA-Z-]+"
SHORT_FLAGS_RE = f"(?P<SHORT_FLAG>{PURE_SHORT_FLAGS_RE})"
LONG_FLAGS_RE = f"(?P<LONG_FLAG>{PURE_LONG_FLAGS_RE})"

# Regular expression for parameters
#!!! Проверить, все ли символы разрешённые в путях вписаны в регулярку
PURE_UNQUOTED_PARAMETERS_RE = r"[a-zA-Zа-яА-ЯёЁ0-9_\-./\\~\(\):]+"
# PURE_QUOTED_PARAMETERS_RE = r"'[a-zA-Zа-яА-ЯёЁ0-9_\-./\\~\(\)]+'|\"[a-zA-Zа-яА-ЯёЁ0-9_\-./\\~\(\)]+\""
PURE_QUOTED_PARAMETERS_RE = r"'[^']*'|\"[^\"]*\""
UNQUOTED_PARAMETERS_RE = f"(?P<UNQUOTED_PARAMETER>{PURE_UNQUOTED_PARAMETERS_RE})"
QUOTED_PARAMETERS_RE = f"(?P<QUOTED_PARAMETER>{PURE_QUOTED_PARAMETERS_RE})"

# Regular expression for all that remained
UNKNOWN_RE = f"(?P<UNKNOWN>.)"
# UNKNOWN1_RE = f"(?P<UNKNOWN1>.)"
# UNKNOWN2_RE = f"(?P<UNKNOWN2>.)"
# UNKNOWN3_RE = f"(?P<UNKNOWN3>.)"
# UNKNOWN4_RE = f"(?P<UNKNOWN4>.)"


# Ordered regular expressions
ALL_EXPRESSIONS = [COMMANDS_RE, LONG_FLAGS_RE, SHORT_FLAGS_RE,
                   QUOTED_PARAMETERS_RE, UNQUOTED_PARAMETERS_RE, SPACE_RE, UNKNOWN_RE]

# Master regular expression to gather all in one
MASTER_RE = re.compile('|'.join(ALL_EXPRESSIONS))
# MASTER_RE = re.compile((COMMANDS_RE | UNKNOWN_RE)((SPACE_RE)+|UNKNOWN_RE)((LONG_FLAGS_RE | SHORT_FLAGS_RE | QUOTED_PARAMETERS_RE | UNQUOTED_PARAMETERS_RE | UNKNOWN_RE)(SPACE_RE | UNKNOWN_RE)+)+)
# MASTER_RE = re.compile(
#     rf"^(?:{COMMANDS_RE}|{UNKNOWN1_RE})"
#     rf"(?:{SPACE_RE}+|{UNKNOWN2_RE})"
#     rf"(?:(?:{LONG_FLAGS_RE}|{SHORT_FLAGS_RE}|{QUOTED_PARAMETERS_RE}|{UNQUOTED_PARAMETERS_RE}|{UNKNOWN3_RE})"
#     rf"(?:{SPACE_RE}+|{UNKNOWN4_RE}))+$"
# )
