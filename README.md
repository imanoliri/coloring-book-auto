# Coloring book auto
This project automatically creates a coloring book for kids from colored images.

## Use
1. Copy images to directory `images`.
2. Install python if you don't have it and all libraries defined in `requirements.txt    `.
3. Open terminal and navigate to the project directory.
4. Run the command `python create_coloring_book.py`
5. Print the file `coloring_book.pdf`


## Image manipulation (using python PIL)
The folder with images in color are read and their colors converted to black or white using a luminosity threshold. The black and white images are copied to `images_black_white`.

The default luminosity threshold is 75 out of 255 (the smaller, the blacker a pixel has to be to be categorized as black). You can change it modifying the variable `LUMINOSITY_THRESHOLD` in the script `create_coloring_book`.

## Document generation (using python fpdf2)
The original images and their black & whites are copied each pair in an horizontal page in a pdf that is then exported to print.

