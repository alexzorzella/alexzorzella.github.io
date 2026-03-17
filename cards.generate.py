from pathlib import Path

def populate_card_page(template:str, output:str, cards:str, use_thumbnails:bool=False):
    project_root = Path(__file__).parent
    template_file = project_root / template
    output_file = project_root / output

    cards_dir = project_root / cards
    card_files = cards_dir.glob(f"*.png")

    code_gen = ""

    code_gen += "<ul>\n"

    for card_file in card_files:
        code_gen += f'<li><a href="{cards}/{card_file.name}"><img src="{cards}/thumbnails/{card_file.name.replace(".png", ".webp")}" alt="{card_file.name}"></a></li>\n'

    code_gen += "</ul>\n"

    with open(template_file, "r") as template_file:
        template = template_file.read()
        template = template.replace("__TEMPLATE__", code_gen)

    with open(output_file, "w") as output:
        output.write(template)

if __name__ == "__main__":
    populate_card_page(template="metafight_cards.template.html", output="cards.html", cards="public/metafight")
    populate_card_page(template="magic_cards.template.html", output="mtg.html", cards="public/mtg", use_thumbnails=True)