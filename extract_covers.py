from pathlib import Path
from shutil import copy

LIBRARY = Path("F:\Calibre Library")
BOOK_PRINTING = Path("F:\Book Printing")

for f in LIBRARY.rglob("cover.jpg"):
    for epub in f.parent.rglob("*.epub"):
        dst_filename = epub.stem + ".jpg"
        pdf_filename = epub.stem + ".pdf"
    for dst_pdf in BOOK_PRINTING.rglob("*" + pdf_filename):
        dst_folder = dst_pdf.parent
        dst_filepath = dst_folder / dst_filename
        copy(f, dst_filepath)