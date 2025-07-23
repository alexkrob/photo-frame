import cv2
import numpy as np
import screeninfo

screen = screeninfo.get_monitors()[0]


def setup_window(window_name: str):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(
        window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


def get_fullscreen_image(filename: str):
    image = cv2.imread(filename)
    image_h, image_w, _ = image.shape

    image_aspect_ratio = image_h/image_w
    monitor_aspect_ratio = screen.height/screen.width

    if monitor_aspect_ratio >= image_aspect_ratio:
        resized_image_w = screen.width
        resized_image_h = round(screen.width * image_aspect_ratio)
        x_offset = 0
        y_offset = round((screen.height - resized_image_h) / 2)
    else:
        resized_image_h = screen.height
        resized_image_w = round(screen.height / image_aspect_ratio)
        y_offset = 0
        x_offset = round((screen.width - resized_image_w) / 2)

    background = np.zeros((screen.height, screen.width, 3), dtype='uint8')
    resized_image = cv2.resize(image, (resized_image_w, resized_image_h))

    background[y_offset: y_offset + resized_image_h,
               x_offset: x_offset + resized_image_w] = resized_image

    return background

def show_image(window_name, image, secs: int):
    cv2.imshow(window_name, image)
    cv2.waitKey(secs * 1000)