import os
from pathlib import Path
from PIL import Image
from multiprocessing import Pool
from dataclasses import dataclass

@dataclass(frozen=True)
class HTMLImageTemplate:
    thumbnail_path: Path | None
    asset_path: Path
    alt:str
    li_class: str | None = None

    def render(self):
        li_class = "" if self.li_class is None else f' class="{self.li_class}"'

        if self.thumbnail_path is not None:
            return f'<li{li_class}><a href="{self.asset_path.as_posix()}"><img src="{self.thumbnail_path.as_posix()}" alt="{self.alt}"></a></li>'
        else:
            return f'<li{li_class}><a href="{self.asset_path.as_posix()}"><img src="{self.asset_path.as_posix()}" alt="{self.alt}"></a></li>'

def populate_gallery(template_file:str, output_file:str, artwork_directory:str):
    code_gen = ""

    project_root = Path(__file__).parent

    directories = [Path(artwork_directory)]

    subdirectories = Path(artwork_directory).iterdir()
    subdirectories = sorted(subdirectories)

    directories.extend(subdirectories)

    for directory in directories:
        if not Path(directory).is_dir() or directory.name == "thumbnails":
            continue

        artwork_files = directory.glob(f"*.png")
        artwork_files = sorted(artwork_files)

        for artwork_file in artwork_files:
            image_path = f"{project_root}/{artwork_file.name}"
            thumbnail_path = f"public/art/thumbnails/{Path(image_path).stem}.webp"

            formatted_image_path = image_path # .replace("\\", "/")

            code_gen += f"""
        <li class="tile"><a href={formatted_image_path}><img fetchpriority="high" src={thumbnail_path} alt="Art"/></a></li>"""

    with open(template_file, "r") as file:
        template = file.read()
        template = template.replace("__TEMPLATE__", code_gen)

    with open(output_file, "w") as output_file:
        output_file.write(template)

    print(f"Populated {Path(template_file).stem} with cards from {artwork_directory}")

def populate_card_page(output_template_filename:str, output_filename:str, card_source_directory_name:str):
    """Creates a populated HTML file given a template, output, and a local directory of cards"""

    project_root = Path(__file__).parent
    output_template_path = project_root / output_template_filename
    output_filepath = project_root / output_filename

    card_source_directory_path = project_root / card_source_directory_name

    directories_to_process = [Path(card_source_directory_path)]

    subdirectories = Path(card_source_directory_path).iterdir()
    subdirectories = sorted(subdirectories)

    directories_to_process.extend(subdirectories)

    html_image_templates: list[HTMLImageTemplate] = []

    for directory in directories_to_process:
        if directory.name == "thumbnails":
            continue

        card_filepaths = directory.glob(f"*.png")

        for card_filepath in card_filepaths:
            thumbnail_path = Path(f'/{card_source_directory_name}/thumbnails/{card_filepath.name.replace(".png", ".webp")}')
            asset_path = Path(f'/{card_source_directory_name}/{directory.relative_to(card_source_directory_path)}/{card_filepath.name}')

            html_image_templates.append(HTMLImageTemplate(thumbnail_path=thumbnail_path, asset_path=asset_path, alt=card_filepath.stem))

    render_and_write_to_template(html_image_templates=html_image_templates, output_template_path=output_template_path, output_filepath=output_filepath)

    print(f"Populated {output_template_path.stem} with cards from {card_source_directory_name}")

def render_and_write_to_template(html_image_templates: list[HTMLImageTemplate], output_template_path: Path, output_filepath: Path):
    code_gen = ""

    code_gen += "<ul>\n"

    for template in html_image_templates:
        code_gen += template.render() + "\n"

    code_gen += "</ul>\n"

    with open(output_template_path, "r") as file:
        template = file.read()
        template = template.replace("__TEMPLATE__", code_gen)

    with open(output_filepath, "w") as output_filename:
        output_filename.write(template)

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
    # create_thumbnails_for_images_recursively("public/art")
    # create_thumbnails_for_images_recursively("public/metafight")
    # create_thumbnails_for_images_recursively("public/mtg")
    populate_gallery(template_file="index.template.html", output_file="index.html", artwork_directory="public/art")
    populate_card_page(output_template_filename="metafight_cards.template.html", output_filename="cards.html", card_source_directory_name="public/metafight")
    populate_card_page(output_template_filename="magic_cards.template.html", output_filename="mtg.html", card_source_directory_name="public/mtg")
