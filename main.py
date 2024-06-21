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
import time

Processor = ImageProcessor(is_init_dnn_superres=True)
Reader = QRCodeProcessor(is_init_qreader=True)
# is_init_qreader: có sử dụng qreader hay không, mặc định là không vì nó tốn thời gian khởi tạo, đọc mã chậm hơn các thư viện khác, đổi lại nó đọc được mã khó và chính xác hơn là lấy được rect và sử dụng roi image

# read image
image = Processor.readImage("./images/test/test.png")

# Processor.showImage("test", image)
# process with super solution (option)
image_processed = Processor.useSuperResolution(image)

detection = Reader.getRectQReader(image_processed)
# print(detection)
# data = Reader.useDecodeQReader(image_processed, detection)
# print(data)

# print("--------test---------")

# get size
# size = Processor.getSizeImage(image_processed)
# print(size)
# 960 x 1280
# try crop

rect = 466, 195, 672, 401  # x1,y1,x2,y2
crop = Processor.cropImage(image_processed, rect, gap=40)
Processor.showImage("test", crop)
print("start")
data = Reader.useDecodeQReaderPyzbar(crop)
print(data)
