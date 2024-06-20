from toolkit.Toolkit import Toolkit
from core.ImageProcessor import ImageProcessor


processor = ImageProcessor()
# image = processor.readImage("./images/test/origin.png")
# processor.showImage("image", image)
# h, w = processor.getSizeImage(image)

# print(h, w)

# crop = processor.cropImage(image, (0, 250, 0, 350))
# processor.saveImage("./images/test/crop.png", crop)
# processor.showImage("crop", crop)


import cv2
import numpy as np

# Đọc ảnh chính và mẫu
image = cv2.imread("./images/test/origin.png")
template = cv2.imread("./images/test/crop.png")

# processor.showImage("origin", image)
# processor.showImage("template", template)

# # Chuyển ảnh chính sang grayscale (ảnh xám)
# # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Lấy kích thước của mẫu
# threshold = 0.9
# w, h = processor.getSizeImage(template)

# # Thực hiện template matching
# result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# x1, y1 = max_loc
# x2, y2 = x1 + w, y1 + h

# if max_val >= threshold:
#     cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 1)

# print(x1, y1, x2, y2)

# # Hiển thị ảnh kết quả
# cv2.imshow("Detected", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


result = processor.templateMatching(image, template, 1, is_show=False)
print(result)
