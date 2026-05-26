import os
import string
from pathlib import Path

valid_chars: str = string.ascii_letters + string.digits + "_."


def format_filenames(path: str = None):
    """Formats a directory's files to be snake_case."""
    while path is None or not Path(path).exists():
        path = input("Filepath: ")

    files = Path(path).rglob("*.*")

    for file in files:
        if not file.is_file():
            continue

        original_filename = file.name
        original_filename = original_filename.lower().strip().replace(" ", "_")

        formatted_name = ""

        for char in original_filename:
            if char in valid_chars:
                formatted_name += char

        os.rename(file.absolute(), file.parent / formatted_name)

        print(f"Renamed {file} to {formatted_name}")


if __name__ == "__main__":
    format_filenames()
