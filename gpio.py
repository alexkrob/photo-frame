import time
from datetime import datetime
from queue import Queue
from enum import Enum


class Edge(Enum):
    RISING = 0
    FALLING = 1


try:
    import RPi.GPIO as GPIO
    gpio_enabled = True
except RuntimeError:
    gpio_enabled = False


if gpio_enabled:
    GPIO.setmode(GPIO.BOARD)


def read_gpio(pin_number: int):
    if gpio_enabled:
        GPIO.setup(pin_number, GPIO.IN)

    try:
        while True:
            if gpio_enabled:
                value = GPIO.input(pin_number)
            else:
                value = 0
            yield value
    except KeyboardInterrupt:
        if gpio_enabled:
            GPIO.cleanup()


def monitor_gpio(pin_number: int, channel: Queue):
    state = 0

    for value in read_gpio(pin_number):
        if state != value:
            channel.put((Edge.RISING if value ==
                        1 else Edge.FALLING,  datetime.now()))
            state = value
        time.sleep(0.1)


if __name__ == '__main__':
    for output in read_gpio(29):
        print(f'{output}')
