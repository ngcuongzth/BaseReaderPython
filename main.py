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

image = Processor.readImage("./images/test/test.png")
image_processed = Processor.useSuperResolution(image)
print("start")
data = Reader.useLoopReader(image=image_processed, iterations=10)
print(data)
