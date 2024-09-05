from PIL import Image
from PIL.ImageFile import ImageFile
import os
from typing import List, Tuple
import pathlib
import json


def image_file_pairs_from_directory(input_dir: str, luminosity_threshold: int):
    return get_save_coloring_image_pairs(
        input_dir,
        filenames_in_directory(input_dir),
        luminosity_threshold,
        f"grayscale/{input_dir}_grayscale",
    )


def filenames_in_directory(directory: str) -> list:
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
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


def load_pages_as_defined_in_content_file(
    input_dir: str, content_file: str, luminosity_threshold: int
) -> list:

    with open(content_file, "rb") as fp:
        book_contents = json.load(fp)

    pages = []
    for keyword, value in book_contents:
        if keyword == "coloring":
            new_pages = image_file_pairs_from_directory(
                f"{input_dir}/{value}", luminosity_threshold
            )
        elif keyword == "image":
            new_pages = [
                f"{input_dir}/{value}/{v}"
                for v in filenames_in_directory(f"{input_dir}/{value}")
            ]
        elif keyword == "blank":
            new_pages = [None] * int(value)
        else:
            ValueError(f"Invalid keyword: {keyword}")
        pages += new_pages

    return pages
