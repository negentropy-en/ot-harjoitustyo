"""Small helper functions for file and path handling"""

import re
from pathlib import Path

# Converting a name into a more simple, safe filename
def make_safe_filename(value):
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    value = value.strip("-")
    if not value:
        return "character"
    return value


def default_export_filename(name, extension):
    safe = make_safe_filename(name)
    return f"{safe}.{extension.lstrip('.')}"


def ensure_directory(path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
