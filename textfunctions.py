## MODULE DEPRECATED, FUNCTIONS MOVED TO functions.py

from colorama import Style

from staticvalues import MAX_PIXEL_VALUE
from mapfunctions import map_invert_intensity_row

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

def print_ascii_matrix(
    ascii_matrix, 
    text_color
):
    for row in ascii_matrix:
        line = [p+p+p for p in row]
        print(text_color + "".join(line))

    print(Style.RESET_ALL)

def normalize_intensity_matrix(
    intensity_matrix
):
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

def invert_intensity_matrix(
    intensity_matrix: list
):
    inverted_intensity_matrix = list(map(map_invert_intensity_row, intensity_matrix))
    return inverted_intensity_matrix

def convert_to_txt(
    matrix: list
):
    with open('tmp.txt','w') as tmp_file:
        for row in matrix:
            tmp_file.write(''.join(row)+'\n')
    with open('tmp.txt', 'r') as tmp_file:
        ascii_text = tmp_file.read()
    return ascii_text