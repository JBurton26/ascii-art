#!/usr/bin/env python
from PIL import Image
import sys, os
from colorama import Fore
import av
import logging

from mapfunctions import map_intensity_row
from staticvalues import ASCII_CHARS
from textfunctions import convert_to_ascii, print_ascii_matrix, normalize_intensity_matrix, invert_intensity_matrix, convert_to_txt
from imgfunctions import draw_image, get_pixel_matrix
from profiler import TimerProfile

av.logging.set_level(av.logging.INFO)
logging.basicConfig(
    filename='./tmp_test.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(funcName)s | %(message)s',
)

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
            with TimerProfile() as timer:
                with av.open(filename) as container:
                    for index, frame in enumerate(container.decode(video=0)):
                        frame_filename = f"out/tmp/frame-{index:04d}.jpg"
                        frame.to_image().save(frame_filename)
                        image = Image.open(frame_filename)
                        pixels = get_pixel_matrix(image)
                        intensity_matrix = list(map(map_intensity_row, pixels))
                        intensity_matrix = normalize_intensity_matrix(intensity_matrix)
                        #intensity_matrix = invert_intensity_matrix(intensity_matrix)

                        ascii_matrix = convert_to_ascii(intensity_matrix, ASCII_CHARS)
                        #print_ascii_matrix(ascii_matrix, Fore.GREEN)
                        #ascii_binary = convert_to_txt(ascii_matrix)
                        new_filename = draw_image(frame_filename, image.size, ascii_matrix)
                        os.remove(frame_filename)
                        image.close()
                    input_codec_name = container.streams.video[0].codec_context.name
                    input_codec_fps = container.streams.video[0].codec_context.rate
                ascii_filename = "out/" + filename.split('.')[0] + ".ascii.mp4"
                ascii_frames = os.listdir('out/tmp/')
                with av.open(ascii_filename, 'w') as container:
                    stream = container.add_stream(input_codec_name, input_codec_fps)
                    stream.width = 1920
                    stream.height = 1080
                    stream.pix_fmt = "yuv420p"
                    for ascii_frame in ascii_frames:
                        image = Image.open(f"out/tmp/{ascii_frame}")
                        frame = av.VideoFrame.from_image(image)
                        for packet in stream.encode(frame):
                            container.mux(packet)
                        image.close()
                        os.remove(f"out/tmp/{ascii_frame}")
                    for packet in stream.encode():
                        container.mux(packet)
                    
        except Exception as e:
            print("Error Occurred while reading file. Exiting.....\n")
            logger.error(e)
            print(e)
            exit
        finally:
            exit

if __name__ == "__main__":
    logger = logging.Logger
    main()