import itertools
import os
from pathlib import Path
from PIL import Image
from multiprocessing import Pool

def populate_gallery(template_file:str, output_file:str, artwork_directory:str):
    code_gen = ""

    subdirectories = Path(artwork_directory).iterdir()
    subdirectories = sorted(subdirectories)

    for subdirectory in subdirectories:
        if not Path(subdirectory).is_dir() or subdirectory.name == "thumbnails":
            continue

        artwork_files = subdirectory.glob(f"*.png")
        artwork_files = sorted(artwork_files)

        for artwork_file in artwork_files:
            image_path = artwork_file
            thumbnail_path = f"public/art/thumbnails/{Path(image_path).stem}.webp"

            formatted_image_path = str(image_path).replace("\\", "/")

            code_gen += f"""
        <li class="tile"><a href={formatted_image_path}><img fetchpriority="high" src={thumbnail_path} alt="Art"/></a></li>"""

    with open(template_file, "r") as file:
        template = file.read()
        template = template.replace("__TEMPLATE__", code_gen)

    with open(output_file, "w") as output_file:
        output_file.write(template)

    print(f"Populated {Path(template_file).stem} with cards from {artwork_directory}")

def populate_card_page(template_file:str, output:str, card_dir:str):
    """Creates a populated HTML file given a template, output, and a local directory of cards"""

    project_root = Path(__file__).parent
    template_file = project_root / template_file
    output_file = project_root / output

    cards_dir = project_root / card_dir
    card_files = cards_dir.glob(f"*.png")

    code_gen = ""

    code_gen += "<ul>\n"

    for card_file in card_files:
        thumbnail_path = f'{card_dir}/thumbnails/{card_file.name.replace(".png", ".webp")}'

        if Path(thumbnail_path).exists():
            image_source = thumbnail_path
            code_gen += f'<li><a href="{card_dir}/{card_file.name}"><img src="{image_source}" alt="{card_file.name}"></a></li>\n'
        else:
            image_source = f"{card_dir}/{card_file.name}"
            code_gen += f'<li><img src="{image_source}" alt="{card_file.name}"></li>\n'

    code_gen += "</ul>\n"

    with open(template_file, "r") as file:
        template = file.read()
        template = template.replace("__TEMPLATE__", code_gen)

    with open(output_file, "w") as output:
        output.write(template)

    print(f"Populated {template_file.stem} with cards from {card_dir}")

def create_thumbnail_for_image(image_path:str, thumbnail_height:int, output_directory:str):
    with Image.open(image_path) as image:
        width, height = image.size

        aspect_ratio = width / height
        new_width = int(thumbnail_height * aspect_ratio)

        resized_image = image.resize((new_width, thumbnail_height), Image.Resampling.LANCZOS)

        output_path = output_directory / f"{image_path.stem}.webp"
        resized_image.save(output_path, "WEBP", quality=100)

def create_thumbnails_for_images_recursively(parent_directory:str, thumbnail_height:int=512):
    output_directory = Path(parent_directory) / "thumbnails"
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    images = Path(parent_directory).rglob("*.png")

    args = [(image_path, thumbnail_height, output_directory) for image_path in images]

    with Pool(processes=os.cpu_count()) as pool:
        pool.starmap(create_thumbnail_for_image, args)

    print(f"Done! {len(args)} thumbnails created for images in {parent_directory}")

if __name__ == "__main__":
    create_thumbnails_for_images_recursively("public/art")
    create_thumbnails_for_images_recursively("public/metafight")
    create_thumbnails_for_images_recursively("public/mtg")
    populate_gallery(template_file="index.template.html", output_file="index.html", artwork_directory="public/art")
    populate_card_page(template_file="metafight_cards.template.html", output="cards.html", card_dir="public/metafight")
    populate_card_page(template_file="magic_cards.template.html", output="mtg.html", card_dir="public/mtg")
