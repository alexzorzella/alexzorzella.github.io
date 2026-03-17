import os
from pathlib import Path

def format_filenames(path: str=None):
    while path is None or not Path(path).exists():
        path = input("Filepath: ")

    files = Path(path).glob("*.*")

    for file in files:
        original_filename = file.name
        formatted_name = \
            f"{original_filename.lower().strip().
            replace(" ", "_").
            replace("\'", "_").
            replace("’", "_").
            replace("&", "and").
            replace(",", "").
            replace("-", "_").
            replace("(", "").
            replace(")", "")}"

        os.rename(file.absolute(), file.parent / formatted_name)

        print(f"Renamed {file} to {formatted_name}")

if __name__ == "__main__":
    format_filenames()