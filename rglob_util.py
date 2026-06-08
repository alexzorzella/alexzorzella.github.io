import csv
import datetime
import glob
import os
from pathlib import Path

from datetime import datetime

def rglob_cards_into_tsv(source: Path, csv_path: Path):
    path = str(source.absolute())
    files = list(filter(os.path.isfile, glob.glob(path + r"/**/*.png", recursive=True)))

    files.sort(key=os.path.getctime)
    files.reverse()

    file_exists = csv_path.is_file()

    entries: set[str] = set()

    if file_exists:
        tsv_lines = csv_path.read_text(encoding='utf-8').splitlines()
        tsv_reader = csv.reader(tsv_lines, delimiter="\t")

        for card in list(tsv_reader)[1:]:
            stem: str = card[0]
            entries.add(stem)

    if not file_exists:
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(f"Id\tName\tApproximate Date Created\tCommentary\n")

    with open(csv_path, "a", encoding="utf-8") as f:
        for file in files:
            filepath = Path(file)
            filename = filepath.stem

            if filename in entries:
                continue

            predicted_name = filename.replace('_', ' ').title().replace("Of", "of").replace("The", "the")

            do_put_comma = input(f"Does '{predicted_name}' get a comma after the first word? (y/n): ").lower() == "y"

            if do_put_comma:
                predicted_name = predicted_name.replace(' ', ", ", 1)

            date_created = datetime.fromtimestamp(os.path.getctime(file)).strftime("%Y/%m/%d")
            f.write(f"{filename}\t{predicted_name}\t{date_created}\t\n")