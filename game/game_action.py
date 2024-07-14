from typing import Tuple

from utils.yolov5 import YoloV5s
from game_control import GameControl
from adb.scrcpy_adb import ScrcpyADB
import time
import cv2 as cv
from ncnn.utils.objects import Detect_Object
import math
import numpy as np


def get_detect_obj_bottom(obj: Detect_Object) -> Tuple[int, int]:
    return int(obj.rect.x + obj.rect.w / 2), int(obj.rect.y + obj.rect.h)


def distance_detect_object(a: Detect_Object, b: Detect_Object):
    return math.sqrt((a.rect.x - b.rect.x) ** 2 + (a.rect.y - b.rect.y) ** 2)


def calc_angle(x1, y1, x2, y2):
    angle = math.atan2(y1 - y2, x1 - x2)
    return 180 - int(angle * 180 / math.pi)


class GameAction:
    def __init__(self, ctrl: GameControl):
        self.ctrl = ctrl
        self.yolo = YoloV5s(target_size=640,
                            prob_threshold=0.25,
                            nms_threshold=0.45,
                            num_threads=4,
                            use_gpu=True)
        self.adb = self.ctrl.adb

    def mov_to_next_room(self):
        t = time.time()
        mov_start = False
        while True:
            time.sleep(0.1)
            screen = self.ctrl.adb.last_screen
            if screen is None:
                continue

            ada_image = cv.adaptiveThreshold(cv.cvtColor(screen, cv.COLOR_BGR2GRAY), 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 13, 3)
            cv.imshow('ada_image', ada_image)
            cv.waitKey(1)
            if np.sum(ada_image) == 0:
                print('过图成功')
                self.adb.touch_end(0, 0)
                return

            result = self.yolo(screen)
            for obj in result:
                color = (0, 255, 0)
                if obj.label == 1:
                    color = (255, 0, 0)
                elif obj.label == 5:
                    color = (0, 0, 255)
                cv.rectangle(screen,
                             (int(obj.rect.x), int(obj.rect.y)),
                             (int(obj.rect.x + obj.rect.w), int(obj.rect.y + + obj.rect.h)),
                             color, 2
                             )
                # print(obj)

            hero = [x for x in result if x.label == 0.0]
            if len(hero) == 0:
                print('没有找到英雄')
                hero = None
                continue
            else:
                hero = hero[0]
                hx, hy = get_detect_obj_bottom(hero)
                cv.circle(screen, (hx, hy), 5, (0, 0, 125), 5)

            arrow = [x for x in result if x.label == 5]
            if len(arrow) == 0:
                continue
            min_distance_arrow = min(arrow, key=lambda a: distance_detect_object(hero, a))

            ax, ay = get_detect_obj_bottom(min_distance_arrow)
            cv.circle(screen, (hx, hy), 5, (0, 255, 0), 5)
            cv.arrowedLine(screen, (hx, hy), (ax, ay), (255, 0, 0), 3)
            angle = calc_angle(hx, hy, ax, ay)
            sx, sy = self.ctrl.calc_mov_point(angle)

            if not mov_start:
                self.adb.touch_start(sx, sy)
                mov_start = True
            else:
                self.adb.touch_move(sx, sy)

            cv.imshow('screen', screen)
            cv.waitKey(1)


if __name__ == '__main__':
    ctrl = GameControl(ScrcpyADB())
    action = GameAction(ctrl)
    while True:
        action.mov_to_next_room()
        time.sleep(3)
