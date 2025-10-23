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
import platform

from staticvalues import ASCII_CHARS, IMAGE_SIZE, VIDEO_RES
#from functions import normalise_intensity_matrix, convert_to_ascii, draw_image
from profiler import TimerProfile
from functions import normalise_intensity_matrix, convert_to_ascii, draw_image, save_all_frames

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
            with TimerProfile() as timer:
                filename = Path(filename).absolute()
                fps = save_all_frames(filename)

                fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
                out_video = cv2.VideoWriter('./out/temp.mp4', fourcc, fps, VIDEO_RES)
                for frame in sorted(os.listdir('./out/tmp/')):
                    image_data = cv2.imread(f"./out/tmp/{frame}")
                    intensity_matrix = normalise_intensity_matrix(image_data, invert)
                    ascii_matrix = convert_to_ascii(intensity_matrix, ASCII_CHARS)
                    if colour:  
                        image = draw_image(IMAGE_SIZE, ascii_matrix, image_data)
                    else:
                        image = draw_image(IMAGE_SIZE, ascii_matrix)
                    
                    os.remove(f"./out/tmp/{frame}")
                    out_video.write(image)

                cv2.destroyAllWindows()
                out_video.release()
                
                out_filename = Path(f'./out/', filename.stem).with_suffix('.ascii.mp4')
                logger.INFO(f'ASCII_OUT_FILE_WITH_AUDIO: {out_filename}')
                
                os.system(f'ffmpeg -y -i "./out/temp.mp4" -i "{filename.absolute()}" -c copy -map 0:0 -map 1:1 -shortest "{out_filename.absolute()}"')
                os.remove("./out/temp.mp4")

        except Exception as e:
            logger.error(f"{type(e)}: {e}", exc_info=True)
            print(e)
            exit

        finally:
            exit

    else:
        try:
            if platform.system() == 'Windows':
                cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
            else:
                cam = cv2.VideoCapture(0)
                
            frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
            logger.info(f"Frame Width: {frame_width}, Frame Height: {frame_height}")
            print(f"Frame Width: {frame_width}, Frame Height: {frame_height}")
            print(f"Press ESC key to exit.")
            while True:
                ret, frame = cam.read()
                frame = cv2.resize(frame, IMAGE_SIZE)
                # image = Image.fromarray(frame)
                # pixels = get_pixel_matrix(image)
                intensity_matrix = normalise_intensity_matrix(frame, invert)
                ascii_matrix = convert_to_ascii(intensity_matrix, ASCII_CHARS)
                # print(f"len(pixels): {len(pixels)}")
                # print(f"len(ascii_matrix): {len(ascii_matrix)}")
                if colour:  
                    image = draw_image(IMAGE_SIZE, ascii_matrix, frame)
                else:
                    image = draw_image(IMAGE_SIZE, ascii_matrix)

                #frame = np.array(image)
                frame = cv2.resize(frame, VIDEO_RES)
                cv2.imshow('Camera', image)
                key_press = cv2.waitKey(1)
                if key_press & 0xFF == 27:
                    break
                if key_press & 0xFF == 32:
                    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                    logger.info(f"Saving screenshot: {current_datetime}.png")
                    cv2.imwrite(f"out/{current_datetime}.png", image)
                    
            # Release the capture and writer objects
            cam.release()
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
        
    main(args.filename, args.webcam, args.invert, args.colour)