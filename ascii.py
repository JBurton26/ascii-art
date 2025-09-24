#!/usr/bin/env python
from PIL import Image
import sys, os
from colorama import Fore
import av
import logging

from staticvalues import ASCII_CHARS
from functions import get_pixel_matrix, normalize_intensity_matrix, convert_to_ascii, draw_image
from profiler import TimerProfile

def main(
        
):
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
                        intensity_matrix = normalize_intensity_matrix(pixels)
                        ascii_matrix = convert_to_ascii(intensity_matrix, ASCII_CHARS)
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
    av.logging.set_level(av.logging.INFO)
    logging.basicConfig(
        filename='./tmp_test.log',
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(funcName)s | %(message)s',
    )
    logger = logging.Logger
    main()