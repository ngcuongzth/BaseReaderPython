"""
Datamatrix Processor
@repository: `https://github.com/ngcuongzth/BaseReaderPython`
@document&libs: OpenCV, Zxingcpp, Pyzbar
@last&update: 2024/06/20
"""

import pylibdmtx.pylibdmtx as dmtx
import zxingcpp
import numpy as np


class DatamatrixProcessor:
    def __init__(self):

        self.name = "Datamatrix Processor"

    def usePylibdmtx(self, frame: np.ndarray, returnRect: bool = False):
        """recommend: nen truyen mot anh da qua xu ly"""
        data = dmtx.decode(frame)

        if returnRect:
            if data:
                x1, y1, x2, y2 = (
                    data[0][1][0],
                    data[0][1][1],
                    data[0][1][2],
                    data[0][1][3],
                )
                return data[0][0].decode("utf-8"), (x1, y1, x2, y2)
            else:
                return None, None
        else:
            if data:
                return data[0][0].decode("utf-8")
            else:
                return None

    def useZxingcpp(self, frame: np.ndarray):

        data = zxingcpp.read_barcodes(frame)
        if len(data) > 0:
            return data[0].text
        return None

    def useLoopReader(self, image: np.ndarray, iterations: int = 2):
        while iterations > 0:
            iterations = iterations - 1
            print(iterations)
            data = self.usePylibdmtx(image)
            if data:
                return data
            else:
                data = self.useZxingcpp(image)
                if data:
                    return data
        return None
