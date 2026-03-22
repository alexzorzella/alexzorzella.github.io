import itertools
import os
from pathlib import Path
from PIL import Image
from multiprocessing import Pool
from dataclasses import dataclass

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
            return f'<li{li_class_name}><a href="{self.asset_path.as_posix()}"><img src="{self.thumbnail_path.as_posix()}" alt="{self.alt}"></a></li>'
        else:
            return f'<li{li_class_name}><a href="{self.asset_path.as_posix()}"><img src="{self.asset_path.as_posix()}" alt="{self.alt}"></a></li>'


def populate_template(
    output_template_filename: str,
    output_filename: str,
    image_sources_directory_name: str,
    ul_class: str | None = None,
    li_class: str | None = None,
):
    """Creates a populated HTML file given a template, output, and a local directory of images"""

    project_root = Path(__file__).parent
    output_template_path = project_root / output_template_filename
    output_filepath = project_root / output_filename

    image_sources_directory_path = project_root / image_sources_directory_name

    directories_to_process = [Path(image_sources_directory_path)]

    subdirectories = Path(image_sources_directory_path).iterdir()
    subdirectories = sorted(subdirectories)

    directories_to_process.extend(subdirectories)

    html_image_templates: list[HTMLImageTemplate] = []

    for directory in directories_to_process:
        if directory.name == "thumbnails":
            continue

        card_filepaths = list(
            itertools.chain.from_iterable(
                directory.rglob(pattern) for pattern in image_filetypes
            )
        )

        for card_filepath in card_filepaths:
            thumbnail_path = Path(
                f"/{image_sources_directory_name}/thumbnails/{card_filepath.with_suffix('.webp').name}"
            )
            asset_path = Path(
                f"/{image_sources_directory_name}/{directory.relative_to(image_sources_directory_path)}/{card_filepath.name}"
            )

            html_image_templates.append(
                HTMLImageTemplate(
                    thumbnail_path=thumbnail_path,
                    asset_path=asset_path,
                    alt=card_filepath.stem,
                    li_class=li_class,
                )
            )

    render_and_write_to_template(
        html_image_templates=html_image_templates,
        output_template_path=output_template_path,
        output_filepath=output_filepath,
        ul_class=ul_class,
    )

    print(
        f"Populated {output_template_path.stem} with images from {image_sources_directory_name}"
    )


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

    print(f"Done! {len(args)} thumbnails created for images in {parent_directory}")


if __name__ == "__main__":
    create_thumbnails_for_images_recursively("public/art")
    create_thumbnails_for_images_recursively("public/metafight")
    create_thumbnails_for_images_recursively("public/mtg")
    create_thumbnails_for_images_recursively("public/fine_art_i_like")

    populate_template(
        output_template_filename="index.template.html",
        output_filename="index.html",
        image_sources_directory_name="public/art",
        li_class="tile",
        ul_class="tilelist",
    )
    populate_template(
        output_template_filename="fine_art.template.html",
        output_filename="fine_art.html",
        image_sources_directory_name="public/fine_art_i_like",
        li_class="tile",
        ul_class="tilelist",
    )
    populate_template(
        output_template_filename="metafight_cards.template.html",
        output_filename="cards.html",
        image_sources_directory_name="public/metafight",
    )
    populate_template(
        output_template_filename="magic_cards.template.html",
        output_filename="mtg.html",
        image_sources_directory_name="public/mtg",
    )