from __future__ import annotations
from datetime import datetime
from typing import Any

_COLORS = {
    "DEBUG": "\033[94m",
    "ERROR": "\033[91m",
    "SUCCESS": "\033[92m",
    "TEMPLATE": "\033[95m",
    "EDIT": "\033[93m",
    "INFO": "\033[0m",
    "INSTALL": "\033[96m",
}

def log(message: Any, level: str = "INFO", debug_mode: bool = True) -> None:
    """Simple colored logger."""
    level = level.upper()
    if level == "DEBUG" and not debug_mode:
        return
    ts = datetime.now().strftime("%H:%M:%S")
    color = _COLORS.get(level, "\033[0m")
    print(f"{color}[{ts}] [{level}] {message}\033[0m")
