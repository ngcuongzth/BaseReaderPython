from core.QRCodeProcessor import QRCodeProcessor
from core.ImageProcessor import ImageProcessor
import cv2
import numpy as np
import time


class Toolkit:
    def __init__(self):
        self.name = "Ultilities function"
        self.Reader = QRCodeProcessor(is_init_qreader=False)
        self.Processor = ImageProcessor()
        self.frame = None
        self.cap = None

    # ! SET PROPS CAMERA
    def setFrameSize(self, width: int = 640, height: int = 480):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def setExposureToZero(self):
        self.cap.set(cv2.CAP_PROP_EXPOSURE, 0)

    # ! OPEN CAMERA
    def openCamera(self, index: int = 0, always_detect: bool = False):
        self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        self.setFrameSize(1280, 960)
        if not self.cap.isOpened():
            print("Can't connect camera")
            return
        while True:
            ret, self.frame = self.cap.read()
            if always_detect:
                self.detectQRHanlder()
            if not ret:
                print("Can't receive frame signal")
                break

            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
            if key == 32:  # press space key event
                self.pressSpaceKey(False)
            self.Processor.showImage("frame", self.frame, waitKey=1)
        self.cap.release()
        cv2.destroyAllWindows()

    # ! SPACE PRESS EVENT
    def pressSpaceKey(self, isSaveImage: bool = False):
        self.readFrame(self.frame)
        if isSaveImage:
            self.takeFrame(f"./toolkit/store/images/{time.time()}.png", self.frame)

    # ! SAVE IMAGE
    def takeFrame(self, path: str, frame: np.ndarray):
        self.Processor.saveImage(path, frame)

    #! READER
    def detectQRHanlder(self):
        data, rect = self.Reader.useQReader(self.frame, return_detections=True)
        if rect is not None and len(rect) == 4:
            x1 = rect[0]
            y1 = rect[1]
            x2 = rect[2]
            y2 = rect[3]
            cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                self.frame,
                data,
                (x1 - 30, y1 - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    #! CUSTOM READ HERE
    def readFrame(self, frame):
        data, detect = self.Reader.useQReader(frame, return_detections=True)
        if data is not None:
            print("root data: ", data)
        else:
            sr_frame = self.Processor.useSuperResolution(image=frame, blurSize=3)
            data, detect = self.Reader.useQReader(sr_frame, return_detections=True)
            if data is not None:
                print("data sr: ", data)
            else:
                print("XXXXXXXXXXXXXXXXXXXXX")
