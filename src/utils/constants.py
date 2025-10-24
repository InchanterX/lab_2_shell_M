import os
import re
from src.utils.registry import Registry

USER_HOME_DIR = os.path.expanduser("~")

# Modules data
REGISTRY = Registry().registration()
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
PURE_SHORT_FLAGS_RE = f"-[{''.join(re.escape(short_flag) for short_flag in SHORT_FLAGS)}]+"
PURE_LONG_FLAGS_RE = f"--({'|'.join(re.escape(long_flag) for long_flag in LONG_FLAGS)})"
SHORT_FLAGS_RE = f"(?P<SHORT_FLAG>{PURE_SHORT_FLAGS_RE})"
LONG_FLAGS_RE = f"(?P<LONG_FLAG>{PURE_LONG_FLAGS_RE})"

# Regular expression for parameters
PURE_UNQUOTED_PARAMETERS_RE = r"[a-zA-Zа-яА-ЯёЁ0-9_\-./\\~\(\)]+"
PURE_QUOTED_PARAMETERS_RE = r"'[a-zA-Zа-яА-ЯёЁ0-9_\-./\\~\(\)]+'|\"[a-zA-Zа-яА-ЯёЁ0-9_\-./\\~\(\)]+\""
UNQUOTED_PARAMETERS_RE = f"(?P<UNQUOTED_PARAMETER>{PURE_UNQUOTED_PARAMETERS_RE})"
QUOTED_PARAMETERS_RE = f"(?P<QUOTED_PARAMETER>{PURE_QUOTED_PARAMETERS_RE})"

# Regular expression for all that remained
UNKNOWN_RE = f"(?P<UNKNOWN>.)"

# Ordered regular expressions
ALL_EXPRESSIONS = [COMMANDS_RE, LONG_FLAGS_RE, SHORT_FLAGS_RE,
                   QUOTED_PARAMETERS_RE, UNQUOTED_PARAMETERS_RE, SPACE_RE, UNKNOWN_RE]

# Master regular expression to gather all in one
MASTER_RE = re.compile('|'.join(ALL_EXPRESSIONS))


def tokenize_with_your_code(command_line):
    """Токенизация строки с помощью вашего кода"""
    tokens = []
    for match in MASTER_RE.finditer(command_line):
        group_dict = match.groupdict()
        for token_type, value in group_dict.items():
            if value is not None:
                tokens.append((token_type, value))
    return tokens


# Тестовые строки
test_commands = [
    "ls 'D:\\My folder\\файлы' -la --help",
    "ls '/dir/'another one'/gol' -la --help"
]

print("Токенизация с помощью вашего кода:\n")

for i, cmd in enumerate(test_commands, 1):
    print(f"Строка {i}: {cmd}")
    print("Результат токенизации:")

    tokens = tokenize_with_your_code(cmd)
    for token_type, value in tokens:
        print(f"  {token_type}: {repr(value)}")

    print("\n" + "="*50 + "\n")

# SHORT_FLAGS = [flag for flag in FLAGS if len(flag) == 1]
# LONG_FLAGS = [flag for flag in FLAGS if len(flag) > 1]

# # Regular components
# COMMANDS_RE = rf"(?P<COMMAND>{'|'.join(re.escape(name) for name in NAMES)})"

# SHORT_FLAGS_RE = rf"(?P<FLAG>-[{re.escape(''.join(SHORT_FLAGS))}]+)"
# LONG_FLAGS_RE = rf"(?P<FLAG>--[{re.escape('|'.join(LONG_FLAGS))}]+)"
# if SHORT_FLAGS and LONG_FLAGS:
#     FLAGS_RE = rf"(?:{SHORT_FLAGS_RE}|{LONG_FLAGS})"
# elif SHORT_FLAGS_RE:
#     FLAGS_RE = SHORT_FLAGS_RE
# elif LONG_FLAGS_RE:
#     FLAGS_RE = LONG_FLAGS_RE
# else:
#     FLAGS_RE = ""

# UNQUOTED_PARAMETERS = r"""(?P<PARAMETER_UNQUOTED>(?:"[^"]*"|'[^']*'))"""
# QUOTED_PARAMETERS = r"""(?P<PARAMETER_QUOTED>[a-zA-ZА-Яа-яЁё0-9_\-./\\]+)"""
# PARAMETERS_RE = rf"(?:{QUOTED_PARAMETERS}|{UNQUOTED_PARAMETERS})"

# SPACE_RE = r"\s+"
# UNKNOWN_RE = r"(?P<UNKNOWN>[^\s]+)"

# # Master regular expression
# MASTER_RE = re.compile(
#     rf"{COMMANDS_RE}|{FLAGS_RE}|{PARAMETERS_RE}|{SPACE_RE}|{UNKNOWN_RE}"
# )

# #!!! Этот код надо потом убрать, он тестовый
# # --- Тест ---
# command = r"ls 'D:\My folder\файлы' -la --help"
# tokens = [m.groupdict() for m in MASTER_RE.finditer(command)]
# print(tokens)

# command = r"ls '/dir/'another one'/gol' -la --help"
# tokens = [m.groupdict() for m in MASTER_RE.finditer(command)]
# print(tokens)
