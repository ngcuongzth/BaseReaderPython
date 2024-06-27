from core.PreprocessorDecode import PreProcessingImage
from core.QRCodeProcessor import QRCodeProcessor
from core.InitModels import init_wechatqrcode, init_dnn_superres
from core.ImageProcessor import ImageProcessor
from core.BarcodeProcessor import BarcodeProcessor
import os, sys
from pyzbar.pyzbar import decode
import numpy as np
from qreader.qreader import QReader as QReaderRoot

reader = QReaderRoot()


# config wechat
# wechat_detector = init_wechatqrcode()

# tiền xử lý ảnh của qreader
IMGProcessor = ImageProcessor(is_init_dnn_superres=True)
Reader = PreProcessingImage(is_use_wechat=True)

MyReader = QRCodeProcessor(is_init_qreader=True)

import time


def read_code(option: int = 1):
    count = 0
    # 1. wechatqrcode
    # 2. zxingcpp
    # 3. pyzbar

    # path_qr = (
    #     r"D:\NguyenCuong\discovery\BaseReaderPython\images\qrcode\qrcode.png"  # 151
    # )
    path_qr = "./images/test/1/notfound.png"
    # path_qr = "./images/image_test"  # 151

    # stime = time.time()
    image = IMGProcessor.readImage(path_qr)
    gray = IMGProcessor.useSuperResolution(image)
    gray = IMGProcessor.medianBlurImage(image=gray, kernel=3)
    gray = IMGProcessor.convertToGrayscale(image)

    # IMGProcessor.showImage("w", gray, waitKey=1)

    # stime = time.perf_counter()
    stime = time.time()

    # print("starttttttttttt")
    # """preprocessor qreader + libs"""
    # data_decode = Reader.readQRCodeProcessor(gray, type=option)
    # if data_decode is None:
    #     print("xxxxxxxxxxxxxxxxxx")
    # else:
    #     count += 1
    #     print("DATA: ", data_decode)

    # print("time: ", (time.perf_counter() - stime))

    # """preprocessor qreader +  3 libs"""
    # # both
    data_decode = Reader.readQRCodeProcessor(gray, type=1)
    if data_decode is not None:
        print("DATA: ", data_decode)
        count += 1
    else:
        data_decode = Reader.readQRCodeProcessor(gray, type=2)
        if data_decode is not None:
            print("DATA", data_decode)
            count += 1
        else:
            data_decode = Reader.readQRCodeProcessor(gray, type=3)
            if data_decode is not None:
                print("DATA", data_decode)
                count += 1
            else:
                print("xxxxxxxxxxxxxxxxxxxxx")

    print(time.time() - stime)

    # print(f"result: {count}/151\n Time AVERAGE: {(time.time() - stime)/151}s ")
    # print(f"result: {count}/151\n Time AVERAGE: {(time.time() - stime)}s ")


# read_code(option=3)


def read_code_qreader():
    count = 0

    # path_qr = r"D:\NguyenCuong\discovery\BaseReaderPython\images\test\1\1.png"  # 151
    path_qr = r"D:\NguyenCuong\discovery\BaseReaderPython\images\image_test\1024x1024.jpeg"  # 151
    path_qr2 = (
        r"D:\NguyenCuong\discovery\BaseReaderPython\images\qrcode\qrcode.png"  # 151
    )

    image = IMGProcessor.readImage(path_qr)
    # gray = IMGProcessor.useSuperResolution(image)
    # gray = IMGProcessor.medianBlurImage(image=gray, kernel=3)
    # gray = IMGProcessor.convertToGrayscale(image)
    import cv2

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    stime = time.time()
    # test_rect = reader.detect(image)
    test_rect = MyReader.getRectQReader(image)
    print("time detect", time.time() - stime)
    print(test_rect)

    data_decode, rect = reader.detect_and_decode(image, return_detections=True)
    rect_s = time.time()
    rect = MyReader.getRectQReader(image)
    print("rect_time", time.time() - rect_s)

    if data_decode is not None and data_decode != (None,) and data_decode != ():
        print("DATA: ", data_decode[0])
        print(time.time() - stime)
        count += 1
    else:
        print("xxxxxxxxxxxxxxx")

    # print(time.time() - stime)


read_code_qreader()
