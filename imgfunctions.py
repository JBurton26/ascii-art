from PIL import Image, ImageDraw, ImageFont
from staticvalues import IMAGE_SIZE
from colorama import Fore
import textwrap
def get_pixel_matrix(
        image:Image
        ) -> list:
    image.thumbnail(IMAGE_SIZE)
    pixels = list(image.getdata())
    return [pixels[i:i+image.width] for i in range(0, len(pixels), image.width)]


def draw_image(
        old_filename: str,
        size: tuple,
        ascii_matrix: list
        ):
    new_filename = old_filename.split('.')[0] + '.ascii.png'

    font = ImageFont.truetype("C:\\Windows\\Fonts\\lucon.ttf", 12)
    image_width, image_height = size
    #text = textwrap.fill(ascii_matrix, image_width)
    image_width = image_width * 9
    image_height = image_height * 16

    image = Image.new("RGBA", (image_width,image_height), "white")
    drawn_image = ImageDraw.Draw(image)


    #ascii_width = drawn_image.textlength(ascii_matrix, font=font)
    #ascii_height = 10 * ascii_matrix.count('\n')
    print(ascii_matrix)
    y=0
    for line in ascii_matrix:
        drawn_image.text((0,y), ''.join(line), fill=(0,255,0), font=font)
        y += 10

    image.save(new_filename, "PNG")