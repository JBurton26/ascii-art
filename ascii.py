#!/usr/bin/env python
from PIL import Image
import os
import cv2
import av
import logging
import argparse
import numpy as np
from staticvalues import ASCII_CHARS
#from functions import normalise_intensity_matrix, convert_to_ascii, draw_image
from profiler import TimerProfile
from functions import get_pixel_matrix, normalise_intensity_matrix, convert_to_ascii, draw_image

logger = logging.getLogger(__name__)

def main(
    filename: str = None,
    webcam: bool = False,
    invert: bool = False,
    colour: bool = False,
):
    av.logging.set_level(av.logging.INFO)
    logging.basicConfig(
        filename='./tmp_test.log',
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(funcName)s | %(message)s',
    )
    print(f"filename: {filename}")
    print(f"webcam: {webcam}")
    print(f"invert: {invert}")
    print(f"colour: {colour}")

    if not webcam:
        try:
            with av.open(filename) as container:
                for index, frame in enumerate(container.decode(video=0)):
                    frame_filename = f"out/tmp/frame-{index:04d}.jpg"
                    frame.to_image().save(frame_filename)
                    image = Image.open(frame_filename)
                    pixels = get_pixel_matrix(image)
                    intensity_matrix = normalise_intensity_matrix(pixels, invert)
                    ascii_matrix = convert_to_ascii(intensity_matrix, ASCII_CHARS)
                    if colour:  
                        image = draw_image(image.size, ascii_matrix, pixels)
                    else:
                        image = draw_image(image.size, ascii_matrix)
                    new_filename = frame_filename.split('.')[0] + '.ascii.png'
                    image.save(new_filename, "PNG")
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
    else:
        try:
            cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
            frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(f"Frame Width: {frame_width}, Frame Height: {frame_height}")
            print(f"Press ESC key to exit.")
            while True:
                ret, frame = cam.read()
                image = Image.fromarray(frame)
                pixels = get_pixel_matrix(image)
                intensity_matrix = normalise_intensity_matrix(pixels, invert)
                ascii_matrix = convert_to_ascii(intensity_matrix, ASCII_CHARS)
                # print(f"len(pixels): {len(pixels)}")
                # print(f"len(ascii_matrix): {len(ascii_matrix)}")
                if colour:  
                    image = draw_image(image.size, ascii_matrix, pixels)
                else:
                    image = draw_image(image.size, ascii_matrix)

                frame = np.array(image)
                cv2.imshow('Camera', frame)

                if cv2.waitKey(1) == 27:
                    break

            # Release the capture and writer objects
            cam.release()
            # out.release()
            cv2.destroyAllWindows()
        except:
            logger.error(f"{type(e)}: {e}", exc_info=True)
            print(e)
            exit
        finally:
            exit


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", dest="filename", default=None, type=str)
    parser.add_argument("-wc", "--webcam", dest="webcam", default=False, type=bool)
    parser.add_argument("--invert", dest="invert", action='store_true')
    parser.add_argument("--colour", dest="colour", action='store_true')
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
        exit
    with TimerProfile() as timer:
        main(args.filename, args.webcam, args.invert, args.colour)