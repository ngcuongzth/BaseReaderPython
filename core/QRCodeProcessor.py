"""
QRCode Processor
@repository: `https://github.com/ngcuongzth/BaseReaderPython`
@document&libs: OpenCV, Qreader, Zxingcpp, Pyzbar, WechatQRCode
@last&update: 2024/06/20
"""

from qreader.qreader import QReader
import cv2
from core.InitModels import init_wechatqrcode
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol
import zxingcpp
from core.ImageProcessor import ImageProcessor


class QRCodeProcessor:
    def __init__(self, is_init_qreader: bool = False):
        self.accept_init_qreader = is_init_qreader
        if is_init_qreader:
            self.qreader = QReader(model_size="n")
            image_temp = cv2.imread("core/assets/temp.png")
            self.qreader.detector.detect(image=image_temp, is_bgr=False)
            self.accept_init_qreader = True
        self.wechat_qrcode_detector = init_wechatqrcode()
        self.processor = ImageProcessor(is_init_dnn_superres=True)

    def useQReader(self, image: np.ndarray, return_detections: bool = False):
        """
        Dùng để giải mã mã QRCode, sử dụng qreader (https://pypi.org/project/qreader)
        Các tham số:
            + image: hình ảnh đầu vào
            + return_detections: (boolean - True/False) - is return detections ?
        Output: decode_text or (decode_text, detect)
        """
        # convert BGR to RGB
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if self.accept_init_qreader:
            if return_detections:
                decoded_text, detect = self.qreader.detect_and_decode(
                    image=image,
                    return_detections=True,
                )
                if detect:
                    rect = detect[0]["bbox_xyxy"].astype(int)
                    return decoded_text[0], rect
                else:
                    return None, None

            else:
                decoded_text = self.qreader.detect_and_decode(
                    image=image, return_detections=False
                )
                if len(decoded_text) > 0 and decoded_text[0] is not None:
                    return decoded_text[0]
                return None
        else:
            raise Exception("Init Callback ? - just.ngcuong")

    def useWeChatQRCode(self, image: np.ndarray):
        res, _ = self.wechat_qrcode_detector.detectAndDecode(image)
        if len(res):
            return res[0]
        else:
            return None

    def usePyzbar(self, image: np.ndarray):
        decoded_data = decode(image, symbols=[ZBarSymbol.QRCODE])
        if len(decoded_data) > 0:
            return decoded_data[0].data.decode("utf-8")
        return None

    def useZxingCpp(self, image: np.ndarray):
        data_decodeded = zxingcpp.read_barcodes(image)
        if len(data_decodeded) > 0:
            return data_decodeded[0].text
        return None

    def getRectQReader(self, image: np.ndarray):
        rect = self.qreader.detect(image=image)
        if rect:
            # rect = rect[0]["bbox_xyxy"]
            # x1, y1, x2, y2 = rect
            # return tuple([x1, y1, x2, y2])
            # return rect[0]
            return rect[0]["bbox_xyxy"]
        return None

    def useQReaderProcessorDecode(self, cropImage, type: int = 1):
        """type decode:\n
        -> 1: use WeChatQRCode\n
        -> 2: use ZxingCpp\n
        -> 3: use Pyzbar\n
        """
        return self.qreader.readQRCodeProcessor(cropImage, type=type)

    def useLoopReader(self, image: np.ndarray, iterations: int = 2):
        # def useLoopReader(self, image: np.ndarray):

        """
        Custom lai o day
        Su dung vong lap de read code
        """

        if iterations < 1:
            raise Exception("So lan lap phai > 0")
        while iterations > 0:
            print("loop remaining: ", iterations)
            # try read by Zxingpp
            iterations = iterations - 1
            data_decoded = self.useQReaderProcessorDecode(image, type=2)
            if data_decoded:
                return data_decoded
        return None
