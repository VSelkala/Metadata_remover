import sys
from pathlib import Path
from PIL import Image


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
OUTPUT_FOLDER_NAME = "Metadata_removed"


def remove_metadata(file_path: Path) -> bool:
    """Create a metadata-free copy of an image."""

    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        print(f"[SKIP] Unsupported file type: {file_path.name}")
        return False

    if not file_path.is_file():
        print(f"[SKIP] File not found: {file_path}")
        return False

    output_folder = file_path.parent / OUTPUT_FOLDER_NAME
    output_folder.mkdir(exist_ok=True)

    output_path = output_folder / file_path.name

    try:
        with Image.open(file_path) as image:
            # Kopioidaan vain kuvadata, jotta EXIF-tiedot yms eivät tule mukana.
            clean_image = Image.new(image.mode, image.size)
            clean_image.paste(image)

            # Muunnetaan tarvittaessa JPEG-tiedosto RGB-muotoon.
            if file_path.suffix.lower() in {".jpg", ".jpeg"}:
                if clean_image.mode not in ("RGB", "L"):
                    clean_image = clean_image.convert("RGB")

                clean_image.save(
                    output_path,
                    format="JPEG",
                    quality=95,
                    optimize=True
                )

            # PNG
            else:
                clean_image.save(
                    output_path,
                    format="PNG",
                    optimize=True
                )

        print(f"[OK] {file_path.name} -> {output_path}")

        return True

    except Exception as error:
        print(f"[ERROR] {file_path.name}: {error}")
        return False


def main():
    # Raahatut tiedostot muutetaan komentoriviargumenteiksi.
    files = [Path(argument) for argument in sys.argv[1:]]

    if not files:
        print("No files were provided.")
        print("Drag JPG or PNG files onto this program.")
        input("\nPress Enter to exit...")
        return

    print("Metadata Remover")
    print("=" * 40)

    success_count = 0

    for file_path in files:
        if remove_metadata(file_path):
            success_count += 1

    print("=" * 40)
    print(f"Finished. {success_count}/{len(files)} file(s) processed.")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
