from PIL import Image
from PIL.ImageFile import ImageFile
import os
from fpdf import FPDF
from typing import List, Tuple
import pathlib


LUMINOSITY_THRESHOLD = 75


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


def create_coloring_book(
    image_pairs: List[Tuple[str]],
    dim_hor: int = 297,
    dim_ver: int = 210,
    margin: int = 25,
) -> FPDF:
    pdf = FPDF(orientation="landscape", unit="mm", format="A4")
    center_pos_img_color = (dim_hor / 2 - dim_hor / 4, dim_ver / 2)
    center_pos_img_bw = (dim_hor / 2 + dim_hor / 4, dim_ver / 2)

    image_space = (dim_hor / 2 - margin, dim_ver - margin)

    for img_col_file, img_bw_file in image_pairs:
        pdf.add_page()
        add_image_in_centered_position(
            pdf, Image.open(img_col_file), image_space, center_pos_img_color
        )
        add_image_in_centered_position(
            pdf, Image.open(img_bw_file), image_space, center_pos_img_bw
        )

    return pdf


def dimensions_image_to_space(img: ImageFile, hdim: int, vdim: int) -> dict:
    h, v = img.size
    img_ratio = h / v
    space_ratio = hdim / vdim

    # either horizontal or vertical is limitant
    if img_ratio > space_ratio:
        return dict(w=hdim, h=hdim / img_ratio)
    return dict(h=vdim, w=vdim * img_ratio)


def add_image_in_centered_position(
    pdf: FPDF, img: Image, space: Tuple[int], center_pos: Tuple[int]
):
    dims = dimensions_image_to_space(img, *space)
    pos_img = get_pos_from_center_pos_and_dimensions(*center_pos, **dims)
    pdf.image(img, *pos_img, **dims)


def get_pos_from_center_pos_and_dimensions(xpos, ypos, w, h) -> Tuple[int]:
    return (xpos - w / 2, ypos - h / 2)


input_dir = "images/color"

img_filenames = filenames_in_directory(input_dir)

image_file_pairs = get_save_coloring_image_pairs(
    input_dir, img_filenames, LUMINOSITY_THRESHOLD, "images/grayscale"
)

pdf_coloring_book = create_coloring_book(image_file_pairs)

pdf_coloring_book.output("coloring_book.pdf")
