import itertools
from pathlib import Path
from PIL import Image

image_filetypes = ["*.png", "*.jpg", "*.jpeg"]

def spring_clean(parent_directory: str):
    images = list(
        itertools.chain.from_iterable(
            Path(parent_directory).rglob(pattern) for pattern in image_filetypes
        )
    )

    processed_image_count: int = 0
    for image_path in images:
        image = Image.open(image_path)
        width, height = image.width, image.height

        if height < 2000:
            continue

        new_width, new_height = width // 2, height // 2

        resize_info = f"{image_path} {width}x{height} to {new_width}x{new_height}"

        do_continue = input(f"Would you like to resize {resize_info}? (y/n): ")

        if do_continue.lower() != "y":
            continue

        half_size = (new_width, new_height)
        resized_image = image.resize(half_size)
        resized_image.save(image_path)

        processed_image_count += 1
        print(f"Resized {resize_info}")

    print(f"Processed {processed_image_count} images")

if __name__ == "__main__":
    spring_clean("./public/mtg/")