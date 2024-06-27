# https://learnopencv.com/super-resolution-in-opencv/#sec3
from qreader.qreader import QReader
import cv2
import os
import time

sr = cv2.dnn_superres.DnnSuperResImpl_create()
path = "models/super_resolution/ESPCN_x3.pb"
sr.readModel(path)
sr.setModel("espcn", 3)

# Create a QReader instance
qreader = QReader(model_size="n")
path = r"./images/image_test"
detector = cv2.wechat_qrcode_WeChatQRCode(
    "models/wechat_qrcode/detect.prototxt",
    "models/wechat_qrcode/detect.caffemodel",
    "models/wechat_qrcode/sr.prototxt",
    "models/wechat_qrcode/sr.caffemodel",
)

cnt_WC = 0
cnt_QR = 0
cnt_RECT = 0
stime = time.time()
for file in os.listdir(path):
    full_path = path + "/" + file
    # Get the image that contains the QR code
    image = cv2.cvtColor(cv2.imread(full_path), cv2.COLOR_BGR2RGB)
    # Use the detect_and_decode function to get the decoded QR data
    decoded_text, detect = qreader.detect_and_decode(
        image=image, return_detections=True
    )

    # if decoded_text is not None and len(detect) > 0:
    if decoded_text is not None and len(detect) > 0 and decoded_text[0]:
        print(decoded_text)
        cnt_RECT += 1
    else:
        continue
    rect = detect[0]["bbox_xyxy"].astype(int)
    # print(rect)
    x = rect[0] - 20
    y = rect[1] - 20
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    roi = image[y : rect[3] + 20, y : rect[2] + 20]
    cv2.imshow("r", roi)
    res, points = detector.detectAndDecode(image)
    if len(res) > 0:
        cnt_WC += 1
        # print("WC:" + res[0])
    if decoded_text[0] is not None:
        cnt_QR += 1
        # print("QR:" + decoded_text[0])
    else:
        # cv2.imshow("IMG", roi)
        result = sr.upsample(roi)
        newImage = cv2.medianBlur(result, 3)
        # cv2.imshow("RES", newImage)
        decoded_text = qreader.detect_and_decode(image=newImage)
        if decoded_text[0] is not None:
            cnt_QR += 1
            print("QR------------:" + decoded_text[0])
    cv2.waitKey(1)
print("time: ", (time.time() - stime) / 151)
print("WC:")
print(cnt_WC)
print("QR:")
print(cnt_QR)
print("RECT:")
print(cnt_RECT)
