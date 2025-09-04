from staticvalues import MAX_PIXEL_VALUE, ASCII_CHARS
def map_invert_intensity_pixel(
        pixel: float
        ) -> float:
    pixel = MAX_PIXEL_VALUE - pixel
    return pixel

def map_invert_intensity_row(
        row: list
        ) -> list:
    inverted_row = list(map(map_invert_intensity_pixel, row))
    return inverted_row

def map_intensity_pixel(
        pixel: tuple
        ) -> int:
    return 0.21 * pixel[0] + 0.72 * pixel[1] + 0.07 * pixel[2]

def map_intensity_row(
        pixels: list
        ) -> list:
    row_intensity = list(map(map_intensity_pixel, pixels))
    return row_intensity