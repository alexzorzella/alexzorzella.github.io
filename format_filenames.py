import os
import string
from pathlib import Path

from colorama import Fore, Style

valid_chars: str = string.ascii_letters + string.digits + "_."

def filename_already_formatted(filename: str) -> bool:
    if " " not in filename and filename.lower() == filename:
        return True

    for char in filename:
        if char not in valid_chars:
            return False

    return False

def format_filenames(path: str = None):
    """Formats a directory's files to be snake_case."""
    while path is None or not Path(path).exists():
        path = input("Filepath: ")

    files = Path(path).rglob("*.*")

    reference_path_as: str = Path(path).stem
    print(f"{Fore.CYAN}Formatting filenames recursively relative to {reference_path_as}{Style.RESET_ALL}")

    renamed_file_count: int = 0
    for file in files:
        if not file.is_file():
            continue

        original_filename = file.name

        if filename_already_formatted(filename=original_filename):
            continue

        original_filename = original_filename.lower().strip().replace(" ", "_")

        formatted_name = ""

        for char in original_filename:
            if char in valid_chars:
                formatted_name += char

        os.rename(file.absolute(), file.parent / formatted_name)

        print(f"{Fore.GREEN}Renamed {file} to {formatted_name}{Style.RESET_ALL}")

    if renamed_file_count > 0:
        print(f"{Fore.LIGHTCYAN_EX}Renamed {renamed_file_count} file(s) in {reference_path_as}{Style.RESET_ALL}")
    else:
        print(f"{Fore.LIGHTCYAN_EX}No files were renamed. What a time saver!{Style.RESET_ALL}")

if __name__ == "__main__":
    format_filenames()