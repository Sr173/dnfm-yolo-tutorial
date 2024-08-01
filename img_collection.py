from adb.scrcpy_adb import ScrcpyADB
import time
import cv2 as cv

# 1280 * 720 dpi 320
if __name__ == '__main__':
    adb = ScrcpyADB()

    index = 56

    while True:
        index += 1
        time.sleep(2)
        screen = adb.last_screen
        cv.imwrite(f'img/{index}.png', screen)
