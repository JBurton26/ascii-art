#!/usr/bin/env python
from PIL import Image
import sys
from colorama import Fore, Style

ASCII_CHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
MAX_PIXEL_VALUE = 255

def get_pixel_matrix(image:Image) -> list:
    image.thumbnail((1000, 75))
    pixels = list(image.getdata())
    return [pixels[i:i+image.width] for i in range(0, len(pixels), image.width)]

def map_pixel_intensity(
        pixel: tuple
) -> int:
    return 0.21 * pixel[0] + 0.72 * pixel[1] + 0.07 * pixel[2]

def map_intensity_row(
        pixels: list
) -> list:
    row_intensity = list(map(map_pixel_intensity, pixels))
    return row_intensity


def normalize_intensity_matrix(intensity_matrix):
    normalized_intensity_matrix = []
    max_pixel = max(map(max, intensity_matrix))
    min_pixel = min(map(min, intensity_matrix))

    for row in intensity_matrix:
        rescaled_row = []
        for p in row:
            r = MAX_PIXEL_VALUE * (p - min_pixel) / float(max_pixel - min_pixel)
            rescaled_row.append(r)
        normalized_intensity_matrix.append(rescaled_row)

    return normalized_intensity_matrix

def convert_to_ascii(intensity_matrix, ascii_chars):
    ascii_matrix = []
    for row in intensity_matrix:
        ascii_row = []
        for p in row:
            ascii_row.append(ascii_chars[int(p/MAX_PIXEL_VALUE * len(ascii_chars)) - 1])
        ascii_matrix.append(ascii_row)

    return ascii_matrix


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

def invert_intensity_matrix(intensity_matrix: list):
    inverted_intensity_matrix = list(map(map_invert_intensity_row, intensity_matrix))
    return inverted_intensity_matrix

def print_ascii_matrix(ascii_matrix, text_color):
    for row in ascii_matrix:
        line = [p+p+p for p in row]
        print(text_color + "".join(line))

    print(Style.RESET_ALL)

def main():
    if len(sys.argv) == 1:
        filename = input("Please enter a filename:\n")
    else:
        filename = sys.argv[1]
    if not filename:
        print("No filename entered. Exiting....\n")
        exit
    else:
        try:
            image = Image.open(filename)
            print(f"Image Format: {image.format}.\nImage Size: {image.size}.\nImage Mode: {image.mode}")
            pixels = get_pixel_matrix(image)
            intensity_matrix = list(map(map_intensity_row, pixels))
            intensity_matrix = normalize_intensity_matrix(intensity_matrix)
            intensity_matrix = invert_intensity_matrix(intensity_matrix)
            intensity_matrix = invert_intensity_matrix(intensity_matrix)

            ascii_matrix = convert_to_ascii(intensity_matrix, ASCII_CHARS)
            print_ascii_matrix(ascii_matrix, Fore.GREEN)
        except Exception as e:
            print("Error Occurred while reading file. Exiting.....\n")
            print(e)
            exit

if __name__ == "__main__":
    main()