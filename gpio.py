import time

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


if __name__ == '__main__':
    read_gpio(29)

