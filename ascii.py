#!/usr/bin/env python
from PIL import Image
import os
import cv2
import av
import logging
import argparse
import numpy as np
from datetime import datetime
from pathlib import Path
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
            filename = Path(filename).absolute()
            with av.open(f'{filename}') as container:
                for index, frame in enumerate(container.decode(video=0)):
                    frame_filename = Path(f"./out/tmp/frame-{index:04d}.jpg").absolute()
                    frame.to_image().save(frame_filename)
                    image = Image.open(frame_filename)
                    pixels = get_pixel_matrix(image)
                    intensity_matrix = normalise_intensity_matrix(pixels, invert)
                    ascii_matrix = convert_to_ascii(intensity_matrix, ASCII_CHARS)
                    if colour:  
                        image = draw_image(image.size, ascii_matrix, pixels)
                    else:
                        image = draw_image(image.size, ascii_matrix)
                    new_filename = frame_filename.with_suffix('.ascii.png')
                    image.save(new_filename, "PNG")
                    os.remove(frame_filename)
                    image.close()
                input_codec_name = container.streams.video[0].codec_context.name
                input_codec_fps = container.streams.video[0].codec_context.rate
            temp_filename = Path("./out/temp.mp4")
            ascii_frames = os.listdir('./out/tmp/')

            with av.open(str(temp_filename), 'w') as container:
                stream = container.add_stream(input_codec_name, input_codec_fps)
                stream.width = 1920
                stream.height = 1080
                stream.pix_fmt = "yuv420p"
                for ascii_frame in ascii_frames:
                    image = Image.open(f"./out/tmp/{ascii_frame}")
                    frame = av.VideoFrame.from_image(image)
                    for packet in stream.encode(frame):
                        container.mux(packet)
                    image.close()
                    os.remove(f"./out/tmp/{ascii_frame}")
                for packet in stream.encode():
                    container.mux(packet)
            
            out_filename = Path(f'{str(temp_filename.parent)}', filename.stem).with_suffix('.ascii.mp4')
            logger.debug(f'ASCII_OUT_FILE_WITH_AUDIO: {out_filename}')
            
            os.system(f'ffmpeg -y -i "{temp_filename.absolute()}" -i "{filename.absolute()}" -c copy -map 0:0 -map 1:1 -shortest "{out_filename.absolute()}"')
            os.remove(temp_filename)
        except Exception as e:
            logger.error(f"{type(e)}: {e}", exc_info=True)
            print(e)
            exit
        finally:
            exit
    else:
        try:
            cam = cv2.VideoCapture(0)#,cv2.CAP_DSHOW)
            # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
            logger.info(f"Frame Width: {frame_width}, Frame Height: {frame_height}")
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
                # frame = cv2.resize(frame, (1920,1080))
                cv2.imshow('Camera', frame)
                key_press = cv2.waitKey(1)
                if key_press & 0xFF == 27:
                    break
                if key_press & 0xFF == 32:
                    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                    logger.info(f"Saving screenshot: {current_datetime}.png")
                    cv2.imwrite(f"out/{current_datetime}.png", frame)
                    
            image.close()
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
    parser.add_argument("--webcam", dest="webcam", action='store_true')
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