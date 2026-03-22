from pathlib import Path
from PIL import Image

def populate_gallery(template:str, output:str, artwork_directory:str):
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

    with open(template, "r") as template_file:
        template = template_file.read()
        template = template.replace("__TEMPLATE__", code_gen)

    with open(output, "w") as output:
        output.write(template)

def populate_card_page(template:str, output:str, card_dir:str):
    """Creates a populated HTML file given a template, output, and a local directory of cards"""

    project_root = Path(__file__).parent
    template_file = project_root / template
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

    with open(template_file, "r") as template_file:
        template = template_file.read()
        template = template.replace("__TEMPLATE__", code_gen)

    with open(output_file, "w") as output:
        output.write(template)

def compress_images_into_thumbnails_recursively(parent_directory:str, thumbnail_height:int=512):
    output_directory = Path(parent_directory) / "output"
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    total_images_processed = 0

    for image_path in parent_directory.rglob("*.png"):
        with Image.open(image_path) as image:
            width, height = image.size

            aspect_ratio = width / height
            new_width = int(thumbnail_height * aspect_ratio)

            resized_image = image.resize((new_width, thumbnail_height), Image.Resampling.LANCZOS)

            output_path = output_directory / f"{image_path.stem}.webp"
            resized_image.save(output_path, "WEBP", quality=100)

            print(f"Saved thumbnail for {image_path} to {output_path}")
            total_images_processed += 1

    print(f"Processed {total_images_processed} images")

if __name__ == "__main__":
    compress_images_into_thumbnails_recursively("public/art")
    compress_images_into_thumbnails_recursively("public/metafight")
    compress_images_into_thumbnails_recursively("public/mtg")
    populate_gallery(template="index.template.html", output="index.html", artwork_directory="public/art")
    populate_card_page(template="metafight_cards.template.html", output="cards.html", card_dir="public/metafight")
    populate_card_page(template="magic_cards.template.html", output="mtg.html", card_dir="public/mtg")
