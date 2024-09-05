from images import load_pages_as_defined_in_content_file, filenames_in_directory
from coloring_book import NamedColoringBook
import fpdf

import PyPDF2


COLORING_BOOK_CONTENT_FILE = "coloring_book_contents.json"
LUMINOSITY_THRESHOLD = 75


pages = load_pages_as_defined_in_content_file(
    "images", COLORING_BOOK_CONTENT_FILE, LUMINOSITY_THRESHOLD
)


pdf_coloring_book.output("coloring_book_middle.pdf")


# add front and end pages and export

## gather files
pdfs_to_merge = [
    f"front_pages/{f}"
    for f in filenames_in_directory("front_pages")
    if f.endswith(".pdf")
]
pdfs_to_merge.append("coloring_book_middle.pdf")
pdfs_to_merge += [
    f"back_pages/{f}"
    for f in filenames_in_directory("back_pages")
    if f.endswith(".pdf")
]

## merge files
mergeFile = PyPDF2.PdfMerger()
for fp in pdfs_to_merge:
    mergeFile.append(PyPDF2.PdfReader(fp, "rb"))

mergeFile.write("coloring_book.pdf")
