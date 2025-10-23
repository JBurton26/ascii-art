ASCII_CHARS = " `^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
#ASCII_CHARS = " .:-=+*#%@"
MAX_PIXEL_VALUE = 255
#IMAGE_SIZE = (80, 45)
#IMAGE_SIZE = (96, 54)
IMAGE_SIZE = (160, 90)
#IMAGE_SIZE = (240,160)
#IMAGE_SIZE = (320, 180)
#IMAGE_SIZE = (640, 360)
#IMAGE_SIZE = (2560, 1440) # High 'Resolution', creates a monochromatic 1440p image
def get_video_res():
    w, h = IMAGE_SIZE
    w = w * 10
    h = h * 10
    return (w, h)
VIDEO_RES = get_video_res()

