import itertools
import os
from pathlib import Path

from PIL import Image
from multiprocessing import Pool
from dataclasses import dataclass

from baklava import is_null_or_whitespace
from format_filenames import format_filenames
from spring_cleaning import spring_clean

from colorama import Fore, Style

image_filetypes = ["*.png", "*.jpg", "*.jpeg"]

@dataclass(frozen=True)
class HTMLImageTemplate:
    thumbnail_path: Path | None
    asset_path: Path
    alt: str
    li_class: str | None = None

    def render(self):
        li_class_name = "" if self.li_class is None else f' class="{self.li_class}"'

        if self.thumbnail_path is not None:
            return f'<li{li_class_name} data-search="{self.alt}"><a href="{self.asset_path.as_posix()}"><img src="{self.thumbnail_path.as_posix()}" alt="{self.alt}"></a></li>'
        else:
            return f'<li{li_class_name} data-search="{self.alt}"><a href="{self.asset_path.as_posix()}"><img src="{self.asset_path.as_posix()}" alt="{self.alt}"></a></li>'

def unique_set(iterable, key=None):
    seen = set()

    for item in iterable:
        value = item if key is None else key(item)

        if value not in seen:
            seen.add(value)
            yield item

def populate_template(
    output_template_filename: str,
    output_filename: str,
    image_sources_directory_name: str,
    glob_recursively: bool = False,
    ul_class: str | None = None,
    li_class: str | None = None,
    thumbnail_dir: str | None = None,
    link_tiles_to_html_pages_of_the_same_name_in: str | None = None,
):
    """Creates a populated HTML file given a template, output, and a local directory of images"""

    project_root = Path(__file__).parent
    output_template_path = project_root / output_template_filename
    output_filepath = project_root / output_filename

    image_sources_directory_path = project_root / image_sources_directory_name

    directories_to_process = [Path(image_sources_directory_path)]

    subdirectories = Path(image_sources_directory_path).iterdir()
    subdirectories = sorted(subdirectories)

    for subdirectory in subdirectories:
        if Path(subdirectory).is_dir():
            directories_to_process.append(subdirectory)

    directories_to_process.sort(key=lambda p: p.name)

    image_filepaths = set()
    html_image_templates: list[HTMLImageTemplate] = []

    printable_source_path = Path(image_sources_directory_path)

    if not glob_recursively:
        for directory in directories_to_process:
            if thumbnail_dir is not None and directory.name == thumbnail_dir or directory.name == "thumbnails" or directory.name == "notshown":
                continue

            print(f"{Fore.MAGENTA}Searching {len(directories_to_process)} subdirectories in {printable_source_path}...{Style.RESET_ALL}")

            images = list(itertools.chain.from_iterable(directory.glob(pattern) for pattern in image_filetypes))

            image_name_list: str = ""

            for item in images:
                image_filepaths.add(item)

                image_name_list += f"{Path(item).name}"

                if not is_null_or_whitespace(image_name_list) and item != images[-1]:
                    image_name_list += ", "

            print(f"{Fore.CYAN}Images: {image_name_list}")

            print(f"{Fore.CYAN}Found {len(images)} image filepaths in {directory}{Style.RESET_ALL}")
    else:
        print(f"{Fore.MAGENTA}Recursively globbing {printable_source_path}{Style.RESET_ALL}")

        all = (itertools.chain.from_iterable(Path(image_sources_directory_name).rglob(pattern) for pattern in image_filetypes))
        image_filepaths = list(unique_set(all, key=lambda p: p.name))

    image_filepaths = list(image_filepaths)
    image_filepaths.sort(key=lambda p: p.name)

    for image_filepath in image_filepaths:
        thumbnail_path = ""

        if thumbnail_dir is not None:
            thumbnail_path += thumbnail_dir
        else:
            thumbnail_path += f"/{image_sources_directory_name}/thumbnails"

        thumbnail_path = Path(f"{thumbnail_path}/{image_filepath.with_suffix('.webp').name}")

        if link_tiles_to_html_pages_of_the_same_name_in is None:
            asset_path = Path(
                f"/{image_sources_directory_name}/{image_filepath.parent.absolute().relative_to(image_sources_directory_path)}/{image_filepath.name}")
        else:
            asset_path = Path(f"{link_tiles_to_html_pages_of_the_same_name_in}/{Path(image_filepath).stem}.html")

        html_image_templates.append(
            HTMLImageTemplate(
                thumbnail_path=thumbnail_path,
                asset_path=asset_path,
                alt=image_filepath.stem,
                li_class=li_class,
            )
        )

    render_and_write_to_template(
        html_image_templates=html_image_templates,
        output_template_path=output_template_path,
        output_filepath=output_filepath,
        ul_class=ul_class,
    )

    print(f"{Fore.GREEN}Populated {len(image_filepaths)} {output_template_path.stem} with images from {image_sources_directory_name}{Style.RESET_ALL}")

def render_and_write_to_template(
    html_image_templates: list[HTMLImageTemplate],
    output_template_path: Path,
    output_filepath: Path,
    ul_class: str | None = None,
):
    ul_class_name = "" if ul_class is None else f' class="{ul_class}"'

    code_gen = ""

    code_gen += f"<ul{ul_class_name}>\n"

    for template in html_image_templates:
        code_gen += template.render() + "\n"

    code_gen += "</ul>\n"

    with open(output_template_path, "r") as file:
        template = file.read()
        template = template.replace("__TEMPLATE__", code_gen)

    with open(output_filepath, "w") as output_filename:
        output_filename.write(template)


def create_thumbnail_for_image(
    image_path: str, thumbnail_height: int, output_directory: str
):
    with Image.open(image_path) as image:
        width, height = image.size

        aspect_ratio = width / height
        new_width = int(thumbnail_height * aspect_ratio)

        resized_image = image.resize(
            (new_width, thumbnail_height), Image.Resampling.LANCZOS
        )

        output_path = output_directory / f"{image_path.stem}.webp"
        resized_image.save(output_path, "WEBP", quality=100)


def create_thumbnails_for_images_recursively(
    parent_directory: str, thumbnail_height: int = 512
):
    output_directory = Path(parent_directory) / "thumbnails"
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    images = list(
        itertools.chain.from_iterable(
            Path(parent_directory).rglob(pattern) for pattern in image_filetypes
        )
    )

    args = [(image_path, thumbnail_height, output_directory) for image_path in images]

    with Pool(processes=os.cpu_count()) as pool:
        pool.starmap(create_thumbnail_for_image, args)

    print(f"{Fore.GREEN}Done! {len(args)} thumbnails created for images in {parent_directory}{Style.RESET_ALL}")

def create_page_for_subdirectory_in_directory(
        parent_directory: str,
        output_template_filename: str,
        output_to_directory: str | None = None,
        thumbnail_dir: str | None = None,
        li_class: str | None = None,
        ul_class: str | None = None):
    if output_to_directory is not None and not Path(output_to_directory).is_dir():
        print(f"{Fore.RED}{output_to_directory} doesn't exist, creating it{Style.RESET_ALL}")
        os.mkdir(output_to_directory)

    directories_processed: int = 0
    for subdirectory in Path(parent_directory).iterdir():
        image_sources_directory_name = str(subdirectory)
        stem = Path(subdirectory).stem
        output_filename = f"{stem}.html"

        if output_to_directory is not None:
            output_filename = f"{output_to_directory}/{output_filename}"

        populate_template(
            output_template_filename=output_template_filename,
            output_filename=output_filename,
            image_sources_directory_name=image_sources_directory_name,
            li_class=li_class,
            ul_class=ul_class,
            thumbnail_dir=thumbnail_dir
        )

        directories_processed += 1

    print(f"{Fore.LIGHTBLUE_EX}Processed {directories_processed} directories{Style.RESET_ALL}")

if __name__ == "__main__":
    format_filenames(r".\public\mtg")

    # create_thumbnails_for_images_recursively("public/fine_art_i_like")
    # create_thumbnails_for_images_recursively("public/art")

    # create_thumbnails_for_images_recursively("public/metafight")

    create_thumbnails_for_images_recursively("public/mtg")
    # create_thumbnails_for_images_recursively("public/universes_beyond_logos")

    create_page_for_subdirectory_in_directory(
        parent_directory="public/mtg",
        output_template_filename="mtg_cards.template.html",
        output_to_directory="mtg_card_pages",
        thumbnail_dir="/public/mtg/thumbnails"
    )

    populate_template(
        output_template_filename="mtg.template.html",
        output_filename="mtg.html",
        image_sources_directory_name="public/universes_beyond_logos",
        li_class="real-size-tile",
        ul_class="tilelist",
        link_tiles_to_html_pages_of_the_same_name_in="/mtg_card_pages"
    )

    populate_template(
        output_template_filename="mtg_search.template.html",
        output_filename="mtg_search.html",
        image_sources_directory_name="public/mtg",
        glob_recursively=True
        # link_tiles_to_html_pages_of_the_same_name_in="public/mtg/"
    )

    spring_clean("./public/mtg/")

    # populate_template(
    #     output_template_filename="index.template.html",
    #     output_filename="index.html",
    #     image_sources_directory_name="public/art",
    #     li_class="tile",
    #     ul_class="tilelist",
    # )

    # populate_template(
    #     output_template_filename="fine_art.template.html",
    #     output_filename="fine_art.html",
    #     image_sources_directory_name="public/fine_art_i_like",
    #     li_class="tile",
    #     ul_class="tilelist",
    # )

    # populate_template(
    #     output_template_filename="metafight_cards.template.html",
    #     output_filename="cards.html",
    #     image_sources_directory_name="public/metafight",
    # )