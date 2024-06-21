# from core.ImageProcessor import ImageProcessor

# processor = ImageProcessor()
# import cv2
# import numpy as np

# image = cv2.imread("./images/test/origin.png")
# template = cv2.imread("./images/test/crop.png")

# result = processor.templateMatching(image, template, 1, is_show=True)
# print(result)


from core.ImageProcessor import ImageProcessor
from core.QRCodeProcessor import QRCodeProcessor

Processor = ImageProcessor(is_init_dnn_superres=True)
Reader = QRCodeProcessor(is_init_qreader=True)
# is_init_qreader: có sử dụng qreader hay không, mặc định là không vì nó tốn thời gian khởi tạo, đọc mã chậm hơn các thư viện khác, đổi lại nó đọc được mã khó và chính xác hơn là lấy được rect và sử dụng roi image

# read image
image = Processor.readImage("./images/qrcode/qrcode.png")
# process with super solution (option)
image_processed = Processor.useSuperResolution(image)
data_decoded = Reader.useQReader(image_processed)
print("data:", data_decoded)  # output: ->  data: SD Team

data_decoded, rect = Reader.useQReader(image_processed, return_detections=True)
if data_decoded:
    print("data and rect: ", data_decoded, rect)
# ouput: => data and rect:  SD Team [108 112 408 411]
