"""
Barcode Processor
@repository: `https://github.com/ngcuongzth/BaseReaderPython`
@document&libs: OpenCV, Zxingcpp, Pyzbar 
@last&update: 2024/06/21
"""

from pyzbar.pyzbar import decode as pyzbarReader, ZBarSymbol
import zxingcpp as zxingReader
import numpy as np


class BarcodeProcessor:
    def __init__(self):
        self.className = "Barcode Processor"

    def useZxingCpp(self, frame: np.ndarray):
        data_decodeded = zxingReader.read_barcodes(frame)
        if len(data_decodeded) > 0:
            return data_decodeded[0].text
        return None

    def usePyzbar(self, frame: np.ndarray):
        decoded_data = pyzbarReader(frame, symbols=[ZBarSymbol.QRCODE])
        if len(decoded_data) > 0:
            return decoded_data[0].data.decode("utf-8")
        return None

    def useLoopReader(self, image: np.ndarray, iterations: int = 2):
        while iterations > 0:
            iterations = iterations - 1
            print(iterations)
            data = self.useZxingCpp(image)
            if data:
                return data
            else:
                data = self.usePyzbar(image)
                if data:
                    return data
        return None
