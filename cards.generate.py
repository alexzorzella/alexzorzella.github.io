from pathlib import Path

def main():
    project_root = Path(__file__).parent
    template_file = project_root / "cards.template.html"
    output_file = project_root / "cards.html"

    cards_dir = project_root / "public/metafight"

    card_files = cards_dir.glob("*.png")
    code_gen = ""

    code_gen += "<ul>\n"

    for card_file in card_files:
        code_gen += f'<li><img src="/public/metafight/{card_file.name}" alt="{card_file.name}"></li>\n'

    code_gen += "</ul>\n"

    with open(template_file, "r") as template_file:
        template = template_file.read()
        template = template.replace("__TEMPLATE__", code_gen)

    with open(output_file, "w") as output:
        output.write(template)

if __name__ == "__main__":
    main()