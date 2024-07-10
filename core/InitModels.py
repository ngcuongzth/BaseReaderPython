"""
Init Models
@repository: `https://github.com/ngcuongzth/BaseReaderPython`
@last&update: 2024/06/20
"""

import cv2


def init_dnn_superres():
    path = "models/super_resolution/ESPCN_x3.pb"
    superres = cv2.dnn_superres.DnnSuperResImpl_create()
    superres.readModel(path)
    superres.setModel("espcn", 3)
    return superres


def init_wechatqrcode():
    detector_wechat = cv2.wechat_qrcode_WeChatQRCode(
        "models/wechat_qrcode/detect.prototxt",
        "models/wechat_qrcode/detect.caffemodel",
        "models/wechat_qrcode/sr.prototxt",
        "models/wechat_qrcode/sr.caffemodel",
    )
    return detector_wechat
