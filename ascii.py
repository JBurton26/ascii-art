#!/usr/bin/env python
from PIL import Image
import sys, os
import av
import logging
import argparse
from staticvalues import ASCII_CHARS
from functions import get_pixel_matrix, normalize_intensity_matrix, convert_to_ascii, draw_image
from profiler import TimerProfile

logger = logging.getLogger(__name__)

def main(
    filename: str = None,
    webcam: bool = False,
    invert: bool = False   
):
    av.logging.set_level(av.logging.INFO)
    logging.basicConfig(
        filename='./tmp_test.log',
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(funcName)s | %(message)s',
    )
    try:
        with av.open(filename) as container:
            for index, frame in enumerate(container.decode(video=0)):
                frame_filename = f"out/tmp/frame-{index:04d}.jpg"
                frame.to_image().save(frame_filename)
                image = Image.open(frame_filename)
                pixels = get_pixel_matrix(image)
                intensity_matrix = normalize_intensity_matrix(pixels, invert)
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
        logger.error(f"{type(e)}: {e}")
        print(e)
        exit
    finally:
        exit

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", dest="filename", default=None, type=str)
    parser.add_argument("-wc", "--webcam", dest="webcam", default=False, type=bool)
    parser.add_argument("-i", "--invert", dest="invert", default=False, type=bool)
    args = parser.parse_args()
    
    if args.filename:
        if not os.path.exists(args.filename):
            logger.error(msg=f"File: {args.filename} does not exist at the path specified.")
            exit
        if args.filename and args.webcam:
            logger.error(msg="Cannot have both a filename and live webcam at the same time.")
            exit
    if not args.filename and not args.webcam:
        logger.error("Must present a filename with '-f FILENAME', or allow live interpolation with '-wc True'.")
    with TimerProfile as timer:
        main(args.filename, args.webcam, args.invert)