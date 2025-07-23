import cv2
import os
import random
import threading
import time
import tomllib
from queue import Queue, Empty


from gpio import *
from image import *

ALLOWED_EXTENSIONS = ['.HEIC', '.JPG', '.PNG']


def main():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    photo_folder = config.get('target_folder', None)

    files = get_files(photo_folder)
    displayed_files = []

    window_name = 'Slideshow'
    setup_window(window_name)

    gpio_pin = config.get('gpio_pin', None)
    gpio_channel = Queue()
    if gpio_pin is not None:
        gpio_monitor_thread = Thread(target=monitor_gpio, args=(gpio_pin, gpio_channel))
        gpio_monitor_thread.start()

    while True:
        try:
            while True:
                activity = gpio_channel.get_nowait()
                print(f'{activity}')
        except Empty:
            pass

        random_file_index = random.randrange(0, len(files))
        displayed_files.append(files[random_file_index])
        image = get_fullscreen_image(displayed_files[-1])
        if image is not None:
            show_image(window_name, image, config.get('seconds_per_photo', 5))
        files = [f for f in get_files(
            photo_folder) if f not in displayed_files]

        if len(files) == 0:
            files = get_files(photo_folder)
            displayed_files = []

    cv2.destroyAllWindows()


def get_files(photo_folder):
    files = [os.path.join(photo_folder, f) for f in os.listdir(photo_folder) if os.path.isfile(os.path.join(
        photo_folder, f)) and os.path.splitext(f)[1].upper() in ALLOWED_EXTENSIONS]

    random.shuffle(files)

    return files


if __name__ == '__main__':
    main()
