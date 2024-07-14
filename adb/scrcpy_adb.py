from adbutils import adb
import scrcpy
import cv2 as cv
import time
from utils.yolov5 import YoloV5s


class ScrcpyADB:
    def __init__(self):
        devices = adb.device_list()
        client = scrcpy.Client(device=devices[0])
        # You can also pass an ADBClient instance to it
        adb.connect("127.0.0.1:5555")
        print(devices, client)
        client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)
        client.start(threaded=True)
        self.client = client
        self.yolo = YoloV5s(target_size=640,
                            prob_threshold=0.25,
                            nms_threshold=0.45,
                            num_threads=4,
                            use_gpu=True)
        self.last_screen = None

    def on_frame(self, frame: cv.Mat):
        if frame is not None:
            self.last_screen = frame
            # try:
            #     result = self.yolo(frame)
            #     for obj in result:
            #         color = (0, 255, 0)
            #         if obj.label == 1:
            #             color = (255, 0, 0)
            #         elif obj.label == 5:
            #             color = (0, 0, 255)
            #
            #         cv.rectangle(frame,
            #                      (int(obj.rect.x), int(obj.rect.y)),
            #                      (int(obj.rect.x + obj.rect.w), int(obj.rect.y + + obj.rect.h)),
            #                      color, 2
            #                      )
            #         print(obj)
            #
            # except Exception as e:
            #     print(e)
            #
            # cv.imshow('frame', frame)
            # cv.waitKey(1)

    def touch_start(self, x: int or float, y: int or float):
        self.client.control.touch(int(x), int(y), scrcpy.ACTION_DOWN)

    def touch_move(self, x: int or float, y: int or float):
        self.client.control.touch(int(x), int(y), scrcpy.ACTION_MOVE)

    def touch_end(self, x: int or float, y: int or float):
        self.client.control.touch(int(x), int(y), scrcpy.ACTION_UP)

    def tap(self, x: int or float, y: int or float):
        self.touch_start(x, y)
        time.sleep(0.01)
        self.touch_end(x, y)


if __name__ == '__main__':
    sadb = ScrcpyADB()
    time.sleep(5)
    sadb.tap(1568 / 1.25, 166 / 1.25)
    time.sleep(999)
