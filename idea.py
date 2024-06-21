# https://learnopencv.com/super-resolution-in-opencv/#sec3


from qreader.qreader import QReader
import cv2
import os
import numpy as np


# def automatic_brightness_and_contrast(image, clip_hist_percent=1):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Calculate grayscale histogram
#     hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
#     hist_size = len(hist)

#     # Calculate cumulative distribution from the histogram
#     accumulator = []
#     accumulator.append(float(hist[0]))
#     for index in range(1, hist_size):
#         accumulator.append(accumulator[index - 1] + float(hist[index]))

#     # Locate points to clip
#     maximum = accumulator[-1]
#     clip_hist_percent *= maximum / 100.0
#     clip_hist_percent /= 2.0

#     # Locate left cut
#     minimum_gray = 0
#     while accumulator[minimum_gray] < clip_hist_percent:
#         minimum_gray += 1

#     # Locate right cut
#     maximum_gray = hist_size - 1
#     while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
#         maximum_gray -= 1

#     # Calculate alpha and beta values
#     alpha = 255 / (maximum_gray - minimum_gray)
#     beta = -minimum_gray * alpha

#     """
#     # Calculate new histogram with desired range and show histogram
#     new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
#     plt.plot(hist)
#     plt.plot(new_hist)
#     plt.xlim([0,256])
#     plt.show()
#     """

#     auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
#     return (auto_result, alpha, beta)


sr = cv2.dnn_superres.DnnSuperResImpl_create()
path = "models/super_resolution/ESPCN_x3.pb"
sr.readModel(path)
sr.setModel("espcn", 3)

# Create a QReader instance
qreader = QReader(model_size="n")

path = r"./red"

detector = cv2.wechat_qrcode_WeChatQRCode(
    "models/wechat_qrcode/detect.prototxt",
    "models/wechat_qrcode/detect.caffemodel",
    "models/wechat_qrcode/sr.prototxt",
    "models/wechat_qrcode/sr.caffemodel",
)
cnt_WC = 0
cnt_QR = 0
cnt_RECT = 0


for file in os.listdir(path):
    full_path = path + "/" + file
    # Get the image that contains the QR code
    image = cv2.cvtColor(cv2.imread(full_path), cv2.COLOR_BGR2RGB)
    # Use the detect_and_decode function to get the decoded QR data
    decoded_text, detect = qreader.detect_and_decode(
        image=image, return_detections=True
    )
    if len(decoded_text) > 0 and decoded_text[0] is not None and len(detect) > 0:
        cnt_RECT += 1
    else:
        continue

    rect = detect[0]["bbox_xyxy"].astype(int)
    print(rect)
    x = rect[0] - 20
    y = rect[1] - 20
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    roi = image[y : rect[3] + 20, y : rect[2] + 20]
    res, points = detector.detectAndDecode(image)
    if len(res) > 0:
        cnt_WC += 1
        print("WC:" + res[0])
    if decoded_text[0] is not None:
        cnt_QR += 1
        print("QR:" + decoded_text[0])
    else:
        cv2.imshow("IMG", roi)
        result = sr.upsample(roi)
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        # newImage = cv2.filter2D(src=result, ddepth=-1, kernel=kernel)
        newImage = cv2.medianBlur(result, 3)
        cv2.imshow("RES", newImage)
        decoded_text = qreader.detect_and_decode(image=newImage)
        if decoded_text[0] is not None:
            cnt_QR += 1
            print("QR------------:" + decoded_text[0])
    cv2.waitKey(1)

    # # Resized image
    # resized = cv2.resize(image,dsize=None,fx=8,fy=8)
    # plt.figure(figsize=(12,8))
    # plt.subplot(1,3,1)
    # # Original image
    # plt.imshow(image[:,:,::-1])
    # plt.subplot(1,3,2)
    # # SR upscaled
    # plt.imshow(result[:,:,::-1])
    # plt.subplot(1,3,3)
    # # OpenCV upscaled
    # plt.imshow(resized[:,:,::-1])
    # plt.show()
print("WC:")
print(cnt_WC)
print("QR:")
print(cnt_QR)
print("RECT:")
print(cnt_RECT)
