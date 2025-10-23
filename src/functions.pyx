import logging 
import cv2
import numpy as np
cimport numpy as cnp

from staticvalues import IMAGE_SIZE, MAX_PIXEL_VALUE

cnp.import_array()
DTYPE = np.int64
ctypedef cnp.int64_t DTYPE_t
logger = logging.getLogger(__name__)

def save_all_frames(filename):
    cap = cv2.VideoCapture(filename)
    if not cap.isOpened():
        return
    total_frames = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    n = 0
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, IMAGE_SIZE, interpolation = cv2.INTER_AREA)
            cv2.imwrite(f"./out/tmp/frame-{str(n).zfill(total_frames)}.jpg", frame)
            n += 1
        else:
            fps = cap.get(cv2.CAP_PROP_FPS)
            cap.release()
            return fps

# def get_pixel_matrix(
#     filename: str
# ):
#     image_data = cv2.imread(filename)
#     image_data = cv2.resize(image_data, IMAGE_SIZE, interpolation = cv2.INTER_AREA)
#     return image_data


def normalise_intensity_matrix(
    pixels: cnp.ndarray,
    invert: bool = False
):
    normalized_intensity_matrix = []
    def map_intensity_row(
            pixels: cnp.ndarray
        ):
            def map_intensity_pixel(
                pixel: cnp.ndarray
            ) -> float:
                return 0.21 * pixel[0] + 0.72 * pixel[1] + 0.07 * pixel[2]
            
            row_intensity = list(map(map_intensity_pixel, pixels))
            return row_intensity
    
    try:
        intensity_matrix = list(map(map_intensity_row, pixels))
        normalized_intensity_matrix = []
        max_pixel = max(map(max, intensity_matrix))
        min_pixel = min(map(min, intensity_matrix))

        for row in intensity_matrix:
            rescaled_row = []
            for p in row:
                r = MAX_PIXEL_VALUE * (p - min_pixel) / float(max_pixel - min_pixel)
                rescaled_row.append(r)
            normalized_intensity_matrix.append(rescaled_row)

        if invert:
            normalized_intensity_matrix = invert_intensity_matrix(normalized_intensity_matrix)
    except Exception as e:
        logger.error(f"{type(e)}: {e}", exc_info=True)
        print(e)
        raise e
    return normalized_intensity_matrix

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
    ascii_matrix: list,
    pixels: cnp.ndarray = None
) -> cnp.ndarray:
    im_width, im_height = size
    im_width = im_width * 10
    im_height = im_height * 10

    img = np.zeros((im_height,im_width,3), np.uint8)
    x = 0
    y = 10
    if pixels is None:
        for row in ascii_matrix:
            for column in row:
                cv2.putText(img, column, (x, y), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=0.9, color=(0,255,0), thickness=1) # color=pixels[x][y],
                x += 10
            x = 0
            y += 10
    else:
        # All rows and columns are of equal length between the ascii matrix and the pixel matrix
        row_length = len(ascii_matrix)
        column_length = len(ascii_matrix[0])
        for row_index in range(row_length):
            for column_index in range(column_length):
                colour = tuple(pixels[row_index][column_index].tolist())
                #print(colour)
                cv2.putText(img, ascii_matrix[row_index][column_index], (x, y), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=0.9, color=colour, thickness=1)
                x += 10
            x = 0
            y += 10
    return img

# def convert_to_txt(
#     matrix: list
# ) -> str:
#     with open('tmp.txt','w') as tmp_file:
#         for row in matrix:
#             tmp_file.write(''.join(row)+'\n')
#     with open('tmp.txt', 'r') as tmp_file:
#         ascii_text = tmp_file.read()
#     return ascii_text
