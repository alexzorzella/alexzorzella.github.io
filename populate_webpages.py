import csv
import datetime
import itertools
import os
from pathlib import Path

from PIL import Image
from multiprocessing import Pool
from dataclasses import dataclass, field

from baklava import is_null_or_whitespace
from format_filenames import format_filenames
from spring_cleaning import spring_clean

from colorama import Fore, Style

image_filetypes = ["*.png", "*.jpg", "*.jpeg"]


@dataclass(frozen=True)
class AssetWithThumbnail:
    thumbnail_path: Path | None
    asset_path: Path
    alt: str

    def get_visual(self):
        return self.thumbnail_path.as_posix() if self.thumbnail_path is not None else self.asset_path.as_posix()


@dataclass(frozen=True)
class HTMLImageTemplate:
    card_front: AssetWithThumbnail
    card_back: AssetWithThumbnail | None = None
    li_class: str | None = None

    def render(self):
        data_search = self.card_front.alt
        asset_path = self.card_front.asset_path.as_posix()

        front_image_path = self.card_front.get_visual()

        is_double_faced = self.card_back is not None

        if is_double_faced:
            data_search = self.card_back.alt  # Back alt name contains front alt name

            back_image_path = self.card_back.get_visual()

            children = [create_element(
                "a",
                {"href": asset_path},
                children=[
                    create_element("img", {"src": front_image_path, "alt": data_search, "class": "flip__card-front"}),
                    create_element("img", {"src": back_image_path, "alt": data_search, "class": "flip__card-back"})
                ]
            )]
        else:
            children = [create_element(
                "a",
                {"href": asset_path},
                children=[
                    create_element("img", {"src": front_image_path, "alt": data_search})
                ]
            )]

        return create_element(
            tag_name='li',
            attributes={"data-search": data_search, "class": self.li_class,
                        "data-card-type": "double_faced" if is_double_faced else None},
            children=children)


def create_element(tag_name: str, attributes: dict[str, str | None], children: list[str] | None = None,
                   self_closing: bool = False) -> str:
    if self_closing:
        assert children is None, "Self closing tags must not have children"

    if children is None:
        child_str = ""
    else:
        child_str = "\n".join(children)

    attribute_str = ""

    for attribute, value in attributes.items():
        if value is not None:
            attribute_str += f'{attribute}="{value}" '

    tag_str = f'<{tag_name} {attribute_str}>{child_str}'

    if self_closing:
        tag_str += f'</{tag_name}>'

    return tag_str


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

    double_sided_cards_fronts_to_backs: dict[str, Path] = {}

    for image_filepath in image_filepaths:
        cardname = image_filepath.stem
        back_char_index = cardname.find("_back_")

        if back_char_index >= 0:
            front_cardname = cardname[:back_char_index]
            double_sided_cards_fronts_to_backs[front_cardname] = Path(image_filepath)

    for image_filepath in image_filepaths:
        if "_back_" in Path(image_filepath).stem:
            continue

        thumbnail_path, asset_path = get_thumbnail_and_asset_paths(
            thumbnail_dir=thumbnail_dir,
            image_sources_directory_name=image_sources_directory_name,
            image_filepath=image_filepath,
            link_tiles_to_html_pages_of_the_same_name_in=link_tiles_to_html_pages_of_the_same_name_in,
            image_sources_directory_path=image_sources_directory_path)

        card_front = AssetWithThumbnail(thumbnail_path=thumbnail_path, asset_path=asset_path, alt=image_filepath.stem)
        card_back = None

        if (back_filepath := double_sided_cards_fronts_to_backs.get(Path(image_filepath).stem)) is not None:
            back_thumbnail_path, back_asset_path = get_thumbnail_and_asset_paths(
                thumbnail_dir=thumbnail_dir,
                image_sources_directory_name=image_sources_directory_name,
                image_filepath=back_filepath,
                link_tiles_to_html_pages_of_the_same_name_in=link_tiles_to_html_pages_of_the_same_name_in,
                image_sources_directory_path=image_sources_directory_path)

            card_back = AssetWithThumbnail(thumbnail_path=back_thumbnail_path, asset_path=back_asset_path,
                                           alt=back_filepath.stem)

        html_image_template = HTMLImageTemplate(card_front=card_front, card_back=card_back, li_class=li_class)

        html_image_templates.append(html_image_template)

    render_and_write_to_template(
        html_image_templates=html_image_templates,
        output_template_path=output_template_path,
        output_filepath=output_filepath,
        ul_class=ul_class,
    )

    print(
        f"{Fore.GREEN}Populated {len(image_filepaths)} {output_template_path.stem} with images from {image_sources_directory_name}{Style.RESET_ALL}")


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


@dataclass(frozen=True)
class MtgCard:
    id: str
    name: str
    thumbnail_path: Path
    created_at: datetime.datetime
    commentary: str | None = None
    article_paragraphs: list[str] = field(default_factory=list)

def populate_individual_mtg_pages(tsv_path: Path,
                                  mtg_card_search_root_path: Path,
                                  newspaper_search_root_path: Path,
                                  card_template_path: Path,
                                  output_dir_path: Path):
    tsv_lines = tsv_path.read_text().splitlines()
    tsv_reader = csv.reader(tsv_lines, delimiter="\t")

    card_stem_to_thumbnail_path: dict[str, Path] = {}
    for file in mtg_card_search_root_path.rglob("*.webp"):
        assert file.stem not in card_stem_to_thumbnail_path, "Duplicate stem found in mtg_card_search_root_path"
        card_stem_to_thumbnail_path[file.stem] = file

    card_stem_to_newspaper: dict[str, Path] = {}

    print(", ".join([file.as_posix() for file in newspaper_search_root_path.rglob("*.txt")]))

    for file in newspaper_search_root_path.rglob("*.txt"):
        assert file.stem not in card_stem_to_newspaper, f"Duplicate stem found in mtg_card_search_root_path: {file.as_posix()}"
        print(f"Found {file}!")
        card_stem_to_newspaper[file.stem] = file

    cards: list[MtgCard] = []
    for card in list(tsv_reader)[1:]:
        stem: str = card[0]
        created_at_str: str = card[1]
        commentary: str = card[2]

        thumbnail_path = card_stem_to_thumbnail_path[stem]

        article_path = card_stem_to_newspaper.get(stem)
        article_paragraphs = []

        if article_path is not None:
            article_paragraphs = article_path.read_text().strip().splitlines()

        cards.append(MtgCard(
            id=stem,
            name=stem.replace("_", " "),
            commentary=commentary or None,
            thumbnail_path=thumbnail_path,
            created_at=datetime.datetime.strptime(created_at_str, "%Y/%m/%d"),
            article_paragraphs=article_paragraphs
        ))

    for card in cards:
        render_and_write_individual_mtg_page(card, card_template_path=card_template_path,
                                   output_file_path=output_dir_path / (card.id + ".html"))


def render_and_write_individual_mtg_page(card: MtgCard, card_template_path: Path, output_file_path: Path):
    with open(card_template_path, "r") as file:
        template = file.read()
        template = template.replace("__TITLE__", card.name)
        template = template.replace("__ID__", card.id)
        template = template.replace("__THUMBNAIL__", card.thumbnail_path.as_posix())
        template = template.replace("__COMMENTARY__", card.commentary or "")
        template = template.replace("__CONTENT__", "\n".join([create_element("p", {}, [paragraph]) for paragraph in card.article_paragraphs]))

        output_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file_path, "w") as output_file_path:
            output_file_path.write(template)

if __name__ == "__main__":
    format_filenames(r".\public\mtg")

    # create_thumbnails_for_images_recursively("public/fine_art_i_like")
    # create_thumbnails_for_images_recursively("public/art")

    # create_thumbnails_for_images_recursively("public/metafight")

    create_thumbnails_for_images_recursively("public/mtg")
    create_thumbnails_for_images_recursively("public/universes_beyond_logos")

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

    populate_individual_mtg_pages(
        card_template_path=Path("./mtg_card_page.template.html"),
        mtg_card_search_root_path=Path("./public/mtg/"),
        newspaper_search_root_path=Path("./public/mtg_card_info/"),
        tsv_path=Path("./public/cardinfo.tsv"),
        output_dir_path=Path("./dedicated_mtg_cards/")
    )
