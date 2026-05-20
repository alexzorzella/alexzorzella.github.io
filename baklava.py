from datetime import datetime
from enum import Enum
from pathlib import Path

def formatted_time():
    """Returns the time formatted as Y/M/D H:M:S"""

    result = datetime.now()
    result = result.strftime("%Y/%m/%d %H:%M:%S")

    return result

def sanitize_snake_cased_string(string: str) -> str:
    result = string.replace("_", " ").replace("-", " ")

    if len(result) > 3:
        result = result.title()

    return result

def is_null_or_whitespace(string):
    """Returns whether a string is null or whitespace. If the passed object isn't a string, it returns false"""

    if string is None:
        return True

    if not isinstance(string, str):
        return False

    result = False

    if string is None:
        return True

    try:
        result = not string.strip()
    except TypeError:
        print(f"Passed object {string} isn't a string")

    return result

def string_to_float(string):
    if string == "":
        return 0

    try:
        result = float(string)
    except ValueError:
        result = 0

    return result

def string_to_int(string):
    if string == "":
        return 0

    try:
        result = int(string)
    except ValueError:
        result = 0

    return result