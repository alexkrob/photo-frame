import time
from gpio import *

def main():
    for gpio_value in read_gpio(29):
        print(f'{gpio_value}')
        time.sleep(0.1) 


if __name__ == '__main__':
    main()
