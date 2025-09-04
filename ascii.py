#!/usr/bin/env python
from PIL import Image
import sys
from colorama import Fore

from mapfunctions import map_intensity_row
from staticvalues import ASCII_CHARS
from textfunctions import convert_to_ascii, print_ascii_matrix, normalize_intensity_matrix, invert_intensity_matrix, convert_to_txt
from imgfunctions import draw_image, get_pixel_matrix


def main():
    if len(sys.argv) == 1:
        filename = input("Please enter a filename:\n")
    else:
        filename = sys.argv[1]
    if not filename:
        print("No filename entered. Exiting....\n")
        exit
    else:
        # try:
            image = Image.open(filename)
            print(f"Image Format: {image.format}.\nImage Size: {image.size}.\nImage Mode: {image.mode}")
            pixels = get_pixel_matrix(image)
            intensity_matrix = list(map(map_intensity_row, pixels))
            intensity_matrix = normalize_intensity_matrix(intensity_matrix)
            #intensity_matrix = invert_intensity_matrix(intensity_matrix)

            ascii_matrix = convert_to_ascii(intensity_matrix, ASCII_CHARS)
            #print_ascii_matrix(ascii_matrix, Fore.GREEN)
            #ascii_binary = convert_to_txt(ascii_matrix)
            draw_image(filename, image.size, ascii_matrix)

        # except Exception as e:
        #     print("Error Occurred while reading file. Exiting.....\n")
        #     print(e)
        #     exit

if __name__ == "__main__":
    main()