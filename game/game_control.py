import time
from typing import Tuple

from adb.scrcpy_adb import ScrcpyADB
import math


class GameControl:
    def __init__(self, adb: ScrcpyADB):
        self.adb = adb

    def calc_mov_point(self, angle: float) -> Tuple[int, int]:
        rx, ry = (205, 520)
        r = 100

        x = rx + r * math.cos(angle * math.pi / 180)
        y = ry - r * math.sin(angle * math.pi / 180)
        return int(x), int(y)

    def move(self, angle: float, t: float):
        # 计算轮盘x, y坐标
        x, y = self.calc_mov_point(angle)
        self.adb.touch_start(x, y)
        time.sleep(t)
        self.adb.touch_end(x, y)

    def attack(self, t: float = 0.01):
        x, y = (1142, 649)
        self.adb.touch_start(x, y)
        time.sleep(t)
        self.adb.touch_end(x, y)


if __name__ == '__main__':
    ctl = GameControl(ScrcpyADB())
    ctl.move(180, 3)
    time.sleep(0.3)
    ctl.attack()
    time.sleep(0.3)
    ctl.move(270, 5)
    time.sleep(0.3)
    ctl.attack(3)


