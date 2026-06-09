from __future__ import annotations

import csv
import datetime
import itertools
import os
from pathlib import Path

from PIL import Image
from multiprocessing import Pool

from assetwiththumbnail import AssetWithThumbnail
from baklava import is_null_or_whitespace
from format_filenames import format_filenames
from imageelementdata import ImageElementData
from rglob_util import rglob_cards_into_tsv
from spring_cleaning import spring_clean

from colorama import Fore, Style

from webtools import create_element

image_filetypes = ["*.png", "*.jpg", "*.jpeg"]

def unique_set(iterable, key=None):
    seen = set()

    for item in iterable:
        value = item if key is None else key(item)

        if value not in seen:
            seen.add(value)
            yield item

def get_thumbnail_and_asset_paths(
        thumbnail_dir,
        image_sources_directory_name,
        image_filepath,
        link_tiles_to_html_pages_of_the_same_name_in,
        image_sources_directory_path):
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

    return thumbnail_path, asset_path

def populate_template(
        cards: list[ImageElementData],
        output_template_filename: str,
        output_filename: str,
        image_sources_directory_name: str,
        thumbnail_dir: str | None = None,
        ul_class: str | None = None,
        glob_recursively: bool = False,
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

    printable_source_path = Path(image_sources_directory_path)

    if not glob_recursively:
        for directory in directories_to_process:
            if thumbnail_dir is not None and directory.name == thumbnail_dir or directory.name == "thumbnails" or directory.name == "notshown":
                continue

            print(
                f"{Fore.MAGENTA}Searching {len(directories_to_process)} subdirectories in {printable_source_path}...{Style.RESET_ALL}")

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

        all = (itertools.chain.from_iterable(
            Path(image_sources_directory_name).rglob(pattern) for pattern in image_filetypes))
        image_filepaths = list(unique_set(all, key=lambda p: p.name))

    image_filepaths = list(image_filepaths)
    image_filepaths.sort(key=lambda p: p.name)

    final_card_selection: list[ImageElementData] = []

    for image_filepath in image_filepaths:
        card = get_card_by_id(cards=cards, card_id=Path(image_filepath).stem)

        if card is not None:
            final_card_selection.append(card)

    final_card_selection = sorted(final_card_selection, key=lambda item: str(item.front.raw_asset_path))

    render_and_write_to_template(cards=final_card_selection, output_template_path=output_template_path, output_filepath=output_filepath, ul_class=ul_class)

    print(f"{Fore.GREEN}Populated {len(final_card_selection)} {output_template_path.stem} with images from {image_sources_directory_name}{Style.RESET_ALL}")

def get_card_by_id(cards: list[ImageElementData], card_id: str):
    return next((card for card in cards if card.id == card_id), None)

def render_and_write_to_template(
        cards: list[ImageElementData],
        output_template_path: Path,
        output_filepath: Path,
        ul_class: str | None = None):
    ul_class_name = "" if ul_class is None else f' class="{ul_class}"'

    code_gen = ""

    code_gen += f"<ul{ul_class_name}>\n"

    for card in cards:
        code_gen += card.render() + "\n"

    code_gen += "</ul>\n"

    with open(output_template_path, "r") as file:
        template = file.read()
        template = template.replace("__TEMPLATE__", code_gen)

    with open(output_filepath, "w", encoding='utf-8') as output_filename:
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
        cards: list[ImageElementData],
        output_to_directory: str | None = None,
        thumbnail_dir: str | None = None,
        ul_class: str | None = None,
        # li_class: str | None = None,
        # link_to_dedicated_pages: bool = False
):
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
            cards=cards,
            output_template_filename=output_template_filename,
            output_filename=output_filename,
            image_sources_directory_name=image_sources_directory_name,
            ul_class=ul_class,
            thumbnail_dir=thumbnail_dir,
            # li_class=li_class,
            # link_to_dedicated_pages=link_to_dedicated_pages
        )

        directories_processed += 1

    print(f"{Fore.LIGHTBLUE_EX}Processed {directories_processed} directories{Style.RESET_ALL}")

def populate_individual_pages(image_elements: list[ImageElementData], page_template_path: Path, output_dir_path: Path, raw_image: bool = False):
    for image_element in image_elements:
        render_and_write_individual_mtg_page(
            image_element=image_element,
            card_template_path=page_template_path,
            output_file_path=output_dir_path / (image_element.id + ".html"),
            raw_image=raw_image)

def get_image_element_data(
        image_root_dir: Path,
        linked_page_dir: str,
        info_root_dir: Path | None = None,
        tsv_path: Path | None = None,
        li_class: str | None = None) -> list[ImageElementData]:
    # Find the thumbnails
    card_stem_to_thumbnail_path: dict[str, Path] = {}
    for file in image_root_dir.rglob("*.webp"):
        assert file.stem not in card_stem_to_thumbnail_path, "Duplicate stem found in mtg_card_search_root_path"
        card_stem_to_thumbnail_path[file.stem] = file

    # Find the actual images
    card_stem_to_asset_path: dict[str, Path] = {}
    for file in image_root_dir.rglob("*.png"):
        assert file.stem not in card_stem_to_asset_path, "Duplicate stem found in mtg_card_search_root_path"
        card_stem_to_asset_path[file.stem] = file

    # Find the info
    card_stem_to_info: dict[str, Path] = {}

    if info_root_dir is not None:
        for file in info_root_dir.rglob("*.txt"):
            assert file.stem not in card_stem_to_info, f"Duplicate stem found in mtg_card_search_root_path: {file.as_posix()}"
            card_stem_to_info[file.stem] = file

    # Find the backs (if applicable) and the links to the pages with more information
    double_sided_cards_fronts_to_backs: dict[str, Path] = {}
    linked_pages: dict[str, Path] = {}
    for card_stem, asset_filepath in card_stem_to_asset_path.items():
        back_char_index = card_stem.find("_back_")

        if back_char_index >= 0:
            front_card_name = card_stem[:back_char_index]
            double_sided_cards_fronts_to_backs[front_card_name] = asset_filepath

        linked_page: Path | None = Path(f"/{linked_page_dir}/{card_stem}.html")

        if linked_page is not None:
            linked_pages[card_stem] = linked_page

    # Read card info tsv for more information
    tsv_data: dict[str, tuple[str, str, str]] = {}

    if tsv_path is not None:
        tsv_lines = tsv_path.read_text(encoding='utf-8').splitlines()
        tsv_reader = csv.reader(tsv_lines, delimiter="\t")

        raw_tsv_data = list(tsv_reader)[1:]

        for card in raw_tsv_data:
            stem: str = card[0]
            name: str = card[1]
            created_at_str: str = card[2]
            commentary: str = card[3] if len(card) > 3 else ""

            tsv_data[stem] = (name, created_at_str, commentary)

    # Create entries for the image elements
    image_elements: list[ImageElementData] = []

    for stem, asset_path in card_stem_to_asset_path.items():
        if "_back_" in stem:
            continue

        name, created_at_str, commentary = stem, "2026/01/01", ""

        tsv_datum = tsv_data[stem] if tsv_data.get(stem) is not None else None

        if tsv_datum is not None:
            name, created_at_str, commentary = tsv_datum[0], tsv_datum[1], tsv_datum[2]

        assert card_stem_to_asset_path.get(stem) is not None, f"{stem} has no asset"
        assert card_stem_to_thumbnail_path.get(stem) is not None, f"{stem} has no thumbnail"

        raw_asset_path = asset_path

        asset_path = card_stem_to_asset_path[stem]
        thumbnail_path = card_stem_to_thumbnail_path[stem]

        article_path = card_stem_to_info.get(stem)
        article_paragraphs = []

        if article_path is not None:
            article_paragraphs = article_path.read_text().strip().splitlines()

        front: AssetWithThumbnail = AssetWithThumbnail(
            asset_path=asset_path,
            thumbnail_path=thumbnail_path,
            commentary=commentary,
            raw_asset_path=raw_asset_path)
        back: AssetWithThumbnail | None = None

        back_asset = double_sided_cards_fronts_to_backs.get(stem)

        if back_asset is not None:
            back = AssetWithThumbnail(
                thumbnail_path=card_stem_to_thumbnail_path[double_sided_cards_fronts_to_backs[stem].stem],
                asset_path=back_asset,
                commentary=commentary)

        image_element = ImageElementData(
            id=stem,
            name=name,
            front=front,
            back=back,
            created_at=datetime.datetime.strptime(created_at_str, "%Y/%m/%d"),
            article_paragraphs=article_paragraphs,
            linked_page=linked_pages[stem],
            li_class=li_class)

        image_elements.append(image_element)

    image_elements = sorted(image_elements, key=lambda item: str(item.front.raw_asset_path))

    return image_elements

def render_and_write_individual_mtg_page(image_element: ImageElementData, card_template_path: Path, output_file_path: Path, raw_image: bool = False):
    with open(card_template_path, "r") as file:
        template = file.read()

        name = image_element.name
        id = image_element.id
        thumbnail = image_element.get_front_thumbnail()
        commentary = image_element.get_front_commentary()

        rendered_card: str = image_element.render(link_to_raw_asset=True, raw_image=raw_image)

        content = "\n".join([create_element("p", {}, [paragraph]) for paragraph in image_element.article_paragraphs])

        name_element = create_element("div", {}, [
            create_element("h1", {}, [name]),
        ])

        template = template.replace("__META_TITLE__", name)
        template = template.replace("__TITLE__", name_element)
        template = template.replace("__ID__", id)
        template = template.replace("__THUMBNAIL__", thumbnail)
        template = template.replace("__COMMENTARY__", commentary)

        body_div_attributes = { "style": "display: flex; justify-content: center" } if is_null_or_whitespace(content) else {}

        body_element = create_element("div", body_div_attributes, [
            create_element("ul", {}, [rendered_card]) if not raw_image else rendered_card,
            content
        ])

        template = template.replace("__BODY__", body_element)

        output_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file_path, "w", encoding='utf-8') as output_file_path:
            output_file_path.write(template)

if __name__ == "__main__":
    format_filenames(r".\public\mtg")

    create_thumbnails_for_images_recursively("public/mtg")
    create_thumbnails_for_images_recursively("public/universes_beyond_logos")

    card_info_tsv = Path("./public/cardinfo.tsv")
    rglob_cards_into_tsv(source=Path("./public/mtg"), csv_path=card_info_tsv)

    spring_clean("./public/mtg/")

    cards: list[ImageElementData] = get_image_element_data(
        tsv_path=card_info_tsv,
        image_root_dir=Path("./public/mtg/"),
        linked_page_dir="dedicated_mtg_cards",
        info_root_dir=Path("./public/mtg_card_info/")
    )

    collections: list[ImageElementData] = get_image_element_data(
        tsv_path=card_info_tsv,
        image_root_dir=Path("./public/universes_beyond_logos/"),
        linked_page_dir="mtg_card_pages",
        info_root_dir=Path("./public/mtg_card_info/"),
        li_class="real-size-tile"
    )

    # Individual pages
    populate_individual_pages(
        image_elements=cards,
        page_template_path=Path("./mtg_card_page.template.html"),
        output_dir_path=Path("./dedicated_mtg_cards/")
    )

    # Main grid
    populate_template(
        cards=collections,
        output_template_filename="mtg.template.html",
        output_filename="mtg.html",
        image_sources_directory_name="public/universes_beyond_logos",
        ul_class="tilelist"
    )

    # Subpages
    create_page_for_subdirectory_in_directory(
        cards = cards,
        parent_directory="public/mtg",
        output_template_filename="mtg_cards.template.html",
        output_to_directory="mtg_card_pages",
        thumbnail_dir="/public/mtg/thumbnails"
    )

    # Search page
    populate_template(
        cards=cards,
        output_template_filename="mtg_search.template.html",
        output_filename="mtg_search.html",
        image_sources_directory_name="public/mtg",
        glob_recursively=True
    )


    format_filenames(r".\public\mtg")

    create_thumbnails_for_images_recursively("public/art")

    art_info_tsv = Path("./public/artinfo.tsv")
    rglob_cards_into_tsv(source=Path("./public/art"), csv_path=art_info_tsv)

    artwork_image_data: list[ImageElementData] = get_image_element_data(
        tsv_path=art_info_tsv,
        image_root_dir=Path("./public/art/"),
        info_root_dir=Path("./public/art_info/"),
        linked_page_dir="art_pages",
        li_class="tile"
    )

    # Individual pages for artworks
    populate_individual_pages(
        image_elements=artwork_image_data,
        page_template_path=Path("./artwork_page.template.html"),
        output_dir_path=Path("./art_pages/"),
        raw_image=True
    )

    populate_template(
        cards=artwork_image_data,
        output_template_filename="index.template.html",
        output_filename="index.html",
        image_sources_directory_name="public/art",
        ul_class="tilelist"
    )

    # create_thumbnails_for_images_recursively("public/fine_art_i_like")

    # create_thumbnails_for_images_recursively("public/metafight")

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