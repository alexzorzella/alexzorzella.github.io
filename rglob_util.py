import csv
import datetime
import glob
import os
from collections import defaultdict
from pathlib import Path

from datetime import datetime

INFO_CSV = "./public/cardinfo.tsv"

def get_card_commentary():
    dictionary: dict[str, str] = defaultdict(str)

    with open(INFO_CSV, "r", encoding="utf-8") as f:
        for index, line in enumerate(f):
            if index == 0:
                continue

def rglob_cards_into_tsv():
    path = str(Path("./public/mtg").absolute())
    files = list(filter(os.path.isfile, glob.glob(path + r"/**/*.png", recursive=True)))

    files.sort(key=os.path.getctime)
    files.reverse()

    tsv_lines = Path(INFO_CSV).read_text(encoding='utf-8').splitlines()
    tsv_reader = csv.reader(tsv_lines, delimiter="\t")

    entries: set[str] = set()
    for card in list(tsv_reader)[1:]:
        stem: str = card[0]
        entries.add(stem)

    with open(INFO_CSV, "a", encoding="utf-8") as f:
        # f.write(f"Id\tName\tApproximate Date Created\tCommentary\n")

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

    # even: bool = True
    # for file in files:
    #     filepath = Path(file)
    #     filename = filepath.name
    #     date_created = datetime.fromtimestamp(os.path.getctime(file)).strftime("%a %b %d %H:%M:%S %Y")
    #
    #     if even:
    #         line_color = Fore.WHITE
    #     else:
    #         line_color = Fore.LIGHTWHITE_EX
    #
    #     print(f"{line_color}{filename.ljust(100, '.')} | {date_created}{Style.RESET_ALL}")
    #
    #     even = not even

if __name__ == "__main__":
    rglob_cards_into_tsv()