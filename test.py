from core.PreprocessorDecode import PreProcessingImage
from core.QRCodeProcessor import QRCodeProcessor
from core.InitModels import init_wechatqrcode, init_dnn_superres
from core.ImageProcessor import ImageProcessor
from core.BarcodeProcessor import BarcodeProcessor
import os, sys
from pyzbar.pyzbar import decode
import numpy as np
from qreader.qreader import QReader as QReaderRoot

# config wechat
# wechat_detector = init_wechatqrcode()

# tiền xử lý ảnh của qreader
IMGProcessor = ImageProcessor(is_init_dnn_superres=True)
Reader = PreProcessingImage(is_use_wechat=True)

import time


def read_code(option: int = 1):
    count = 0
    # 1. wechatqrcode
    # 2. zxingcpp
    # 3. pyzbar

    path_qr = "./images/image_test"  # 151
    count_time = 0

    for file in os.listdir(path_qr):
        full_path = path_qr + "/" + file
        image = IMGProcessor.readImage(full_path)
        gray = IMGProcessor.useSuperResolution(image)
        gray = IMGProcessor.medianBlurImage(image=gray, kernel=3)
        gray = IMGProcessor.convertToGrayscale(image)

        IMGProcessor.showImage("w", gray, waitKey=1)

        # """preprocessor qreader + libs"""

        # stime = time.time()
        # data_decode = Reader.readQRCodeProcessor(gray, type=option)
        # if data_decode is None:
        #     print("xxxxxxxxxxxxxxxxxx")
        # else:
        #     count += 1
        #     print("DATA: ", data_decode)
        # count_time += time.time() - stime

        """preprocessor qreader +  3 libs"""
        # both
        stime = time.time()
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
        count_time += time.time() - stime

    print(f"result: {count}/151\n Time AVERAGE: {count_time/151}s ")


read_code(3)


""" use qreader preprocessor
WechatQRCode: 139/151 -> speed average: 0.3773074829025774s 
ZxingCpp: 130/151 -> speed average: 0.24254696100752876s 
Pyzbar: 121/151 -> speed average: 0.4047942240506608s 
both: 143/151 -> speed average: 0.4429871688615407s 
"""


QReader = QRCodeProcessor(is_init_qreader=True)
reader = QReaderRoot()


def read_code_qreader():
    count = 0
    count_ps = 0

    path_qr = "./images/image_test"  # 151

    stime = time.time()
    for file in os.listdir(path_qr):
        full_path = path_qr + "/" + file
        image = IMGProcessor.readImage(full_path)
        gray = IMGProcessor.useSuperResolution(image)
        gray = IMGProcessor.medianBlurImage(image=gray, kernel=3)
        gray = IMGProcessor.convertToGrayscale(image)
        import cv2

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # IMGProcessor.showImage("w", gray, waitKey=1)

        rect_s = time.time()
        data_decode = QReader.getRectQReader(gray)
        print("rect time", time.time() - rect_s)
        data_decode, rect = reader.detect_and_decode(image, return_detections=True)

        if data_decode is not None and data_decode != (None,) and data_decode != ():
            # print("DATA: ", data_decode[0])
            count += 1
        else:
            # print("xxxxxxxxxxxxxxx")
            if rect:
                rect = rect[0]["bbox_xyxy"].astype(int)
                x = rect[0] - 20
                y = rect[1] - 20
                if x < 0:
                    x = 0
                if y < 0:
                    y = 0

                roi = image[y : rect[3] + 20, y : rect[2] + 20]

                gray = IMGProcessor.convertToGrayscale(image)

                data_decode = Reader.readQRCodeProcessor(gray, type=1)
                if data_decode is not None:
                    # print("DATA PROCESSED: ", data_decode)
                    # count += 1
                    count_ps += 1
                else:
                    data_decode = Reader.readQRCodeProcessor(gray, type=2)
                    if data_decode is not None:
                        # print("DATA PROCESSED: ", data_decode)
                        # count += 1
                        count_ps += 1
                    else:
                        data_decode = Reader.readQRCodeProcessor(gray, type=3)
                        if data_decode is not None:
                            # print("DATA PROCESSED: ", data_decode)
                            # count += 1
                            count_ps += 1
                        else:
                            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

                # IMGProcessor.showImage("r", roi, 0)

                # data_decode = QReader.useWeChatQRCode(roi)
                # if data_decode is not None:
                #     print("DATA PROCESSED 1: ", data_decode)
                #     # count += 1
                #     count_ps += 1
                # else:
                #     img_processed = IMGProcessor.useSuperResolution(roi)
                #     blur = IMGProcessor.medianBlurImage(img_processed, 3)
                #     data_decode = QReader.useWeChatQRCode(blur)
                #     if data_decode:
                #         print("DATA PROCESSED 2: ", data_decode)
                #     else:
                #         print("xxxxxxxxxxxxxxxx")
            else:
                print("could not found rect")

    print("More: ", count_ps)
    print(f"result: {count }/151\n Time AVERAGE: {(time.time() - stime)/151}s ")
    print("total: ", count + count_ps)


# read_code_qreader()
