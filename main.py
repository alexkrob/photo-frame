import cv2
import os
import random
import time
import tomllib


from gpio import *
from image import get_fullscreen_image, setup_window, show_image

ALLOWED_EXTENSIONS = ['.HEIC', '.JPG', '.PNG']


def main():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    print(f'{config}')
    photo_folder = config.get('target_folder', None)
    files = [os.path.join(photo_folder, f) for f in os.listdir(photo_folder) if os.path.isfile(os.path.join(
        photo_folder, f)) and os.path.splitext(f)[1].upper() in ALLOWED_EXTENSIONS]
    
    random.shuffle(files)

    window_name = 'Slideshow'
    setup_window(window_name)

    for file in files:
        image = get_fullscreen_image(file)
        show_image(window_name, image, config.get('seconds_per_photo', 5))

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
