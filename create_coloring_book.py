from images import load_pages_as_defined_in_content_file
from coloring_book import NamedColoringBook


COLORING_BOOK_CONTENT_FILE = "coloring_book_contents.json"
LUMINOSITY_THRESHOLD = 75


pages = load_pages_as_defined_in_content_file(
    "images", COLORING_BOOK_CONTENT_FILE, LUMINOSITY_THRESHOLD
)

pdf_coloring_book = NamedColoringBook.create_coloring_book(pages, name="Peter Jackson")

pdf_coloring_book.output("coloring_book.pdf")
