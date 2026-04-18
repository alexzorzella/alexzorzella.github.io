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
        new_width, new_height = width // 2, height // 2
        half_size = (new_width, new_height)
        resized_image = image.resize(half_size)
        resized_image.save(image_path)

        processed_image_count += 1
        print(f"Resized {image_path} {width}x{height} to {new_width}x{new_height}")

    print(f"Processed {processed_image_count} images")

if __name__ == "__main__":
    spring_clean("./public/mtg/")