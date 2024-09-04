from PIL import Image
from PIL.ImageFile import ImageFile
from fpdf import FPDF
from typing import List, Tuple


class ColoringBook(FPDF):

    def __init__(
        self, *args, dim_hor: int = 297, dim_ver: int = 210, margin: int = 25, **kwargs
    ) -> "ColoringBook":

        self.dim_hor = dim_hor
        self.dim_ver = dim_ver
        self.margin = margin
        self.center_pos_img_color: Tuple = (dim_hor / 2 - dim_hor / 4, dim_ver / 2)
        self.center_pos_img_bw: Tuple = (dim_hor / 2 + dim_hor / 4, dim_ver / 2)
        self.image_space: Tuple = (dim_hor / 2 - margin, dim_ver - margin)

        super().__init__(*args, **kwargs)

    @classmethod
    def create_coloring_book(
        cls,
        image_pairs: List[Tuple[str]],
        *,
        orientation="landscape",
        unit="mm",
        format="A4",
        **kwargs
    ) -> "ColoringBook":
        pdf = cls(orientation, unit, format, **kwargs)
        pdf = pdf.add_image_pair_pages(image_pairs)
        return pdf

    def add_image_pair_pages(
        self,
        image_pairs: List[Tuple[str]],
    ) -> FPDF:
        for img_col_file, img_bw_file in image_pairs:
            self.add_page()
            self.add_image_in_centered_position(
                Image.open(img_col_file),
                self.image_space,
                self.center_pos_img_color,
            )
            self.add_image_in_centered_position(
                Image.open(img_bw_file),
                self.image_space,
                self.center_pos_img_bw,
            )

        return self

    def add_image_in_centered_position(
        self, img: Image, space: Tuple[int], center_pos: Tuple[int]
    ):
        dims = self.dimensions_image_to_space(img, *space)
        pos_img = self.get_pos_from_center_pos_and_dimensions(*center_pos, **dims)
        self.image(img, *pos_img, **dims)

    @staticmethod
    def dimensions_image_to_space(img: ImageFile, hdim: int, vdim: int) -> dict:
        h, v = img.size
        img_ratio = h / v
        space_ratio = hdim / vdim

        # either horizontal or vertical is limitant
        if img_ratio > space_ratio:
            return dict(w=hdim, h=hdim / img_ratio)
        return dict(h=vdim, w=vdim * img_ratio)

    @staticmethod
    def get_pos_from_center_pos_and_dimensions(xpos, ypos, w, h) -> Tuple[int]:
        return (xpos - w / 2, ypos - h / 2)


class NamedColoringBook(ColoringBook):
    def __init__(self, *args, name: str, **kwargs) -> ColoringBook:
        self.name = name
        super().__init__(*args, **kwargs)

    def header(self):

        self.set_font("Times", "BI", 15)
        # Move to the right & write cell
        self.cell(self.dim_hor - 80)
        self.cell(30, 10, self.name)

        # Line break
        self.ln(20)
