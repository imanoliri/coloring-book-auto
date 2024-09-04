from PIL import Image
from PIL.ImageFile import ImageFile
import os
from typing import List, Tuple
import pathlib

from coloring_book import NamedColoringBook


LUMINOSITY_THRESHOLD = 75


def image_file_pairs_from_directory(input_dir: str):
    return get_save_coloring_image_pairs(
        input_dir,
        filenames_in_directory(input_dir),
        LUMINOSITY_THRESHOLD,
        f"{input_dir}_grayscale",
    )


def filenames_in_directory(directory: str) -> list:
    return [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]


def to_black_and_white(img: ImageFile, threshhold: int = 127) -> Image:
    black_white_binary = lambda x: 255 if x > threshhold else 0
    return img.convert("L").point(black_white_binary, mode="1")


def get_save_coloring_image_pairs(
    input_dir: str, img_filenames: str, threshhold: int, output_dir: str
) -> List[Tuple[ImageFile]]:

    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    image_pair_files = []
    for img_filename in img_filenames:
        img_col_file = f"{input_dir}/{img_filename}"
        img_col = Image.open(img_col_file)

        img_bw = to_black_and_white(img_col, threshhold=threshhold)
        img_bw_file = f"{output_dir}/{img_filename}"
        img_bw.save(img_bw_file)

        image_pair_files.append((img_col_file, img_bw_file))

    return image_pair_files


car_pair_images = image_file_pairs_from_directory("images/cars")
plane_pair_images = image_file_pairs_from_directory("images/planes")
train_pair_images = image_file_pairs_from_directory("images/trains")

blank_pages = [None] * 15
pages = (
    car_pair_images
    + blank_pages
    + plane_pair_images
    + blank_pages
    + train_pair_images
    + blank_pages
)

pdf_coloring_book = NamedColoringBook.create_coloring_book(pages, name="Peter Jackson")

pdf_coloring_book.output("coloring_book.pdf")
