import os
import string
from pathlib import Path

from colorama import Fore, Style

valid_chars: str = string.ascii_letters + string.digits + "_."

def filename_already_formatted_guess(filename: str) -> bool:
    if " " not in filename and filename.lower() == filename:
        return True

    return False

def format_filenames(path: str = None):
    """Formats a directory's files to be snake_case."""
    while path is None or not Path(path).exists():
        path = input("Filepath: ")

    files = Path(path).rglob("*.*")

    for file in files:
        if not file.is_file():
            continue

        original_filename = file.name

        if filename_already_formatted_guess(filename=original_filename):
            continue

        original_filename = original_filename.lower().strip().replace(" ", "_")

        formatted_name = ""

        for char in original_filename:
            if char in valid_chars:
                formatted_name += char

        os.rename(file.absolute(), file.parent / formatted_name)

        print(f"Renamed {file} to {formatted_name}")


if __name__ == "__main__":
    format_filenames()
