import cv2
import time
from gpio import *


def main():
    image = cv2.imread()
    cv2.imshow("Slideshow", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
