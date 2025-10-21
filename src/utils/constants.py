import os
import re
from src.utils.registry import Registry

USER_HOME_DIR = os.path.expanduser("~")

# Modules data
REGISTRY = Registry().registration()
NAMES = list(REGISTRY.keys())
FLAGS = set(flag for name in NAMES for flag in REGISTRY[name]["flags"])

# Regular components
COMMANDS_RE = rf"({'|'.join(re.escape(name) for name in NAMES)})"
FLAGS_RE = rf"({'|'.join(re.escape(flag) for flag in FLAGS)})"
PARAMETERS_RE = r"(?:[a-zA-Z0-9_\-./\\]+(?:\s[a-zA-Z0-9_\-./\\]+)*)"
SPACE_RE = r"\s+"

# Master regular expression
MASTER_RE = re.compile(
    rf"^{COMMANDS_RE}(?:{SPACE_RE}(?:{PARAMETERS_RE}|{FLAGS_RE}))*$")


#!!! Этот код надо убрать, он тестовый
TOKEN_RE = re.compile(
    rf"(?P<COMMAND>{COMMANDS_RE})|(?P<FLAG>{FLAGS_RE})|(?P<PARAM>{PARAMETERS_RE})"
)

command = r"ls \d\repository\ -l"

tokens = []
for m in TOKEN_RE.finditer(command):
    if m.group("COMMAND"):
        tokens.append(("COMMAND", m.group(0)))
    elif m.group("FLAG"):
        tokens.append(("FLAG", m.group(0)))
    elif m.group("PARAM"):
        tokens.append(("PARAM", m.group(0)))

print(tokens)
