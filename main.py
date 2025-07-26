import os
import random
from datetime import timedelta
import logging
from threading import Thread
import tomllib
from queue import Queue, Empty, Full


from gpio import *
from image import *
from display import *

ALLOWED_EXTENSIONS = ['.HEIC', '.JPG', '.PNG']

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s\t%(message)s')


def main():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    photo_folder = config.get('target_folder', None)

    files = get_files(photo_folder)
    queued_files = []

    window_name = 'Slideshow'
    image_channel = Queue(config.get('max_queued_photos', 10))
    display_thread = Thread(target=display, args=(window_name, image_channel))
    display_thread.start()

    gpio_pin = config.get('gpio_pin', None)
    gpio_channel = Queue()
    gpio_activity = None
    if gpio_pin is not None:
        gpio_monitor_thread = Thread(
            target=monitor_gpio, args=(gpio_pin, gpio_channel))
        gpio_monitor_thread.start()

    display_status = DisplayState.ON

    while True:
        try:
            while not gpio_channel.empty():
                gpio_activity = gpio_channel.get_nowait()
                logging.debug(
                    f'Motion sensor triggered {gpio_activity[0]} at {gpio_activity[1]}.')
        except Empty:
            pass

        if gpio_activity is not None:
            edge, timestamp = gpio_activity

            if (edge == Edge.FALLING and
                    datetime.now() - timestamp > timedelta(minutes=config.get('display_inactivity_timeout_mins', 10)) and
                    display_status == DisplayState.ON):
                logging.debug(
                    'Inactivity timeout elapsed. Turning display off.')
                display_status = DisplayState.OFF
                toggle_display(display_status, config.get(
                    'default_display', ':0'))

            if edge == Edge.RISING and display_status == DisplayState.OFF:
                logging.debug('Motion detected. Turning display on.')
                display_status = DisplayState.ON
                toggle_display(display_status, config.get(
                    'default_display', ':0'))

        random_file_index = random.randrange(0, len(files))
        random_file = files[random_file_index]
        image = get_fullscreen_image(random_file)
        queued_new_photo = False

        if image is not None:
            try:
                if not image_channel.full():
                    image_channel.put_nowait(
                        (image, config.get('seconds_per_photo', 5)))
                    queued_files.append(random_file)
                    logging.info(f'Queued {random_file} for display.')
                    queued_new_photo = True
            except Full:
                logging.warning(
                    f'Could not queue {random_file} for display (queue full).')
                pass
        else:
            logging.warning(f'Could not append {random_file} to queue (could not process image).')
            queued_files.append(random_file)
            queued_new_photo = True


        if queued_new_photo:
            files = [f for f in get_files(
                photo_folder) if f not in queued_files]

            logging.info(
                f'Found {len(files)} photos yet to be displayed ({len(queued_files)} already queued).')

        if len(files) == 0:
            files = get_files(photo_folder)
            logging.debug(
                f'Out of files in queue. Refreshing {len(files)} photos.')
            queued_files = []


def get_files(photo_folder):
    files = os.listdir(photo_folder)
    files = [os.path.join(photo_folder, f) for f in files if os.path.splitext(f)[
        1].upper() in ALLOWED_EXTENSIONS]

    random.shuffle(files)

    return files


if __name__ == '__main__':
    main()
