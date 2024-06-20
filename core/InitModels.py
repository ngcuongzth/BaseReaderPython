import cv2


def init_dnn_superres():
    path = "models/super_resolution/ESPCN_x2.pb"
    superres = cv2.dnn_superres.DnnSuperResImpl_create()
    superres.readModel(path)
    superres.setModel("espcn", 2)
    return superres


def init_wechatqrcode():
    detector_wechat = cv2.wechat_qrcode_WeChatQRCode(
        "models/wechat_qrcode/detect.prototxt",
        "models/wechat_qrcode/detect.caffemodel",
        "models/wechat_qrcode/sr.prototxt",
        "models/wechat_qrcode/sr.caffemodel",
    )
    return detector_wechat
