from PIL import Image, ImageDraw, ImageFont

from staticvalues import IMAGE_SIZE

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
    new_filename = 'out/' + old_filename.split('.')[0] + '.ascii.png'

    font = ImageFont.truetype("C:\\Windows\\Fonts\\lucon.ttf", 12)
    image_width, image_height = size
    image_width = image_width * 10
    image_height = image_height * 12

    image = Image.new("RGBA", (image_width,image_height), "black")
    drawn_image = ImageDraw.Draw(image)


    x = 0
    y = 0
    
    for row in ascii_matrix:
        for column in row:
            drawn_image.text((x,y), column, fill=(0,255,0), font=font)
            x += 10
        x = 0
        y += 12

    image.save(new_filename, "PNG")