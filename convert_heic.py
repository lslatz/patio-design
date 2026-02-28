"""
HEIC to JPEG Converter
Converts all .heic/.HEIC files in the 'photos' folder to JPEG.
Output files are saved alongside the originals with a .jpg extension.
"""

import sys
from pathlib import Path

from PIL import Image
import pillow_heif

# Register HEIF opener so Pillow can handle .heic files
pillow_heif.register_heif_opener()

PHOTOS_DIR = Path(__file__).parent / "photos"
JPEG_QUALITY = 95


def convert_heic_to_jpeg(source_dir: Path) -> int:
    """Convert all HEIC files in source_dir to JPEG. Returns count of converted files."""
    heic_files = list(source_dir.glob("*.[hH][eE][iI][cC]"))

    if not heic_files:
        print(f"No HEIC files found in {source_dir}")
        return 0

    converted = 0
    for heic_path in heic_files:
        jpeg_path = heic_path.with_suffix(".jpg")
        try:
            print(f"Converting: {heic_path.name} -> {jpeg_path.name}")
            img = Image.open(heic_path)
            # Preserve EXIF orientation
            exif = img.info.get("exif")
            save_kwargs = {"quality": JPEG_QUALITY}
            if exif:
                save_kwargs["exif"] = exif
            img.save(jpeg_path, "JPEG", **save_kwargs)
            converted += 1
        except Exception as e:
            print(f"  ERROR: {e}", file=sys.stderr)

    return converted


if __name__ == "__main__":
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else PHOTOS_DIR
    if not source.is_dir():
        print(f"Directory not found: {source}", file=sys.stderr)
        sys.exit(1)

    count = convert_heic_to_jpeg(source)
    print(f"\nDone — {count} file(s) converted.")
