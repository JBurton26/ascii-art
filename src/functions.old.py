from PIL import Image, ImageDraw, ImageFont
from staticvalues import IMAGE_SIZE, MAX_PIXEL_VALUE

def get_pixel_matrix(
    image:Image
) -> list:
    image.thumbnail(IMAGE_SIZE)
    pixels = list(image.getdata())
    return [pixels[i:i+image.width] for i in range(0, len(pixels), image.width)]

def normalise_intensity_matrix(
    pixels: list,
    invert: bool = False
) -> list:
    
    def map_intensity_row(
        pixels: list
    ) -> list:
        def map_intensity_pixel(
            pixel: tuple
        ) -> int:
            return 0.21 * pixel[0] + 0.72 * pixel[1] + 0.07 * pixel[2]
        
        row_intensity = list(map(map_intensity_pixel, pixels))
        return row_intensity

    intensity_matrix = list(map(map_intensity_row, pixels))
    normalised_intensity_matrix = []
    max_pixel = max(map(max, intensity_matrix))
    min_pixel = min(map(min, intensity_matrix))

    for row in intensity_matrix:
        rescaled_row = []
        for p in row:
            r = MAX_PIXEL_VALUE * (p - min_pixel) / float(max_pixel - min_pixel)
            rescaled_row.append(r)
        normalised_intensity_matrix.append(rescaled_row)

    if invert:
        normalised_intensity_matrix = invert_intensity_matrix(normalised_intensity_matrix)

    return normalised_intensity_matrix

def invert_intensity_matrix(
    intensity_matrix: list
):
    def map_invert_intensity_row(
        row: list
    ) -> list:
        def map_invert_intensity_pixel(
            pixel: float
        ) -> float:
            pixel = MAX_PIXEL_VALUE - pixel
            return pixel
        
        inverted_row = list(map(map_invert_intensity_pixel, row))
        return inverted_row
    
    inverted_intensity_matrix = list(map(map_invert_intensity_row, intensity_matrix))
    return inverted_intensity_matrix

def convert_to_ascii(
    intensity_matrix, 
    ascii_chars
):
    ascii_matrix = []
    for row in intensity_matrix:
        ascii_row = []
        for p in row:
            ascii_row.append(ascii_chars[int(p/MAX_PIXEL_VALUE * len(ascii_chars)) - 1])
        ascii_matrix.append(ascii_row)

    return ascii_matrix

def draw_image(
    size: tuple,
    ascii_matrix: list
) -> Image:
    

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

    
    return image

# def convert_to_txt(
#     matrix: list
# ) -> str:
#     with open('tmp.txt','w') as tmp_file:
#         for row in matrix:
#             tmp_file.write(''.join(row)+'\n')
#     with open('tmp.txt', 'r') as tmp_file:
#         ascii_text = tmp_file.read()
#     return ascii_text
