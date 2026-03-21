from pathlib import Path

from pdf2image import convert_from_path

def format_filenames(path: str = None):
    """Saves the pages of all PDF files in a directory to PNG files"""
    while path is None or not Path(path).exists() or not Path(path).is_dir():
        path = input("Directory: ")

    pdf_files = Path(path).glob("*.pdf")
    output_dir = Path(path) / "output"

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    total_files = 0

    for pdf in pdf_files:
        images = convert_from_path(pdf, dpi=300)

        for i, image in enumerate(images):
            image_filename = f"{Path(pdf).stem}_{i}.png"
            image.save(Path(output_dir) / image_filename, 'PNG')
            total_files += 1

        print(f"Saved {len(images)} images from {pdf} to {output_dir}")

    print(f"Done! Processed {total_files} total images from {len(pdf_files)} pdf files")

if __name__ == "__main__":
    format_filenames()