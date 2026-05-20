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

def get_string_input(prompt: str, may_be_nothing: bool = False) -> str | None:
    result: str | None = None

    if not may_be_nothing and is_null_or_whitespace(result):
        while is_null_or_whitespace(result):
            result = input(prompt)

    return result

def get_int_input(prompt: str, may_be_nothing: bool = False, min: int | None = None, max: int | None = None) -> int | None:
    while True:
        try:
            result = get_string_input(prompt=prompt, may_be_nothing=may_be_nothing)

            if is_null_or_whitespace(result) and may_be_nothing:
                if result is None:
                    return None
                elif result.strip() == "":
                    return 0

            int_result = int(result)

            if isinstance(min, int) and int_result < min:
                raise ValueError

            if isinstance(max, int) and int_result > max:
                raise ValueError

            return int_result
        except:
            pass