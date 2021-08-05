from urllib.request import urlopen
import cv2
import numpy as np
from threading import Thread
import time

URL = "http://192.168.1.130:8080/shot.jpg"
IMAGE_WIDTH = 800

mac_K = np.array([
            [954.0874994019651, 0                , 660.572082940535  ],
            [0                , 949.9159862376827, 329.78814306885795],
            [0                , 0                , 1                 ]
        ])

oneplus_8t_K = np.array([
            [1.51e3, 0  , 961],
            [0  , 1.51e3, 553],
            [0  , 0  , 1]
        ])

galaxy_s10_K = np.array([[2.00294746e+03, 0, 1.26670666e+03],
                         [0, 1.99399851e+03, 6.09768895e+02],
                         [0, 0, 1]])

elp_K = np.array([
            [9.53e2, 0  , 975],
            [0  , 9.53e2, 550],
            [0  , 0  , 1]
        ])


class RemoteStreamer(Thread):

    def __init__(self, url, K, D=0):
        super(RemoteStreamer, self).__init__()
        self.url = url
        self.img = None
        self.ret = False
        self.is_running = True
        self.K = K
        self.D = D
        self.start()

    def run(self):
        while self.is_running:
            try:
                img_resp = urlopen(self.url)
                img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
                self.img = cv2.imdecode(img_np, -1)
                self.ret = True
            except Exception as e:
                print(e)
                self.ret = False
            # cv2.imshow('temp', cv2.resize(img, (600, 400)))
            # q = cv2.waitKey(1)
            # if q == ord("q"):
            #     break
        # cv2.destroyAllWindows()

    def read(self):
        return self.ret, self.img

    def close(self):
        self.is_running = False


class WebcamStreamer(Thread):

    def __init__(self, camera_number, K, D=0):
        super(WebcamStreamer, self).__init__()
        self.img = None
        self.ret = False
        self.is_running = True
        self.cam = cv2.VideoCapture(camera_number)
        self.K = K
        self.D = D
        time.sleep(0)
        self.start()

    def run(self):
        while self.is_running:
            self.ret, img = self.cam.read()
            if self.ret:
                # print("grabbed frame")
                self.img = img

    def read(self):
        return self.ret, self.img

    def close(self):
        self.is_running = False
        self.cam.release()