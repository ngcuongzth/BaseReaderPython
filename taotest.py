from qreader.qreader import QReader
from cv2 import QRCodeDetector, imread

qreader_reader, cv2_reader, pyzbar_reader = QReader(), QRCodeDetector()

for img_path in (
    "./images/red/1703313890.513911.png",
    "./images/red/1703313650.9005318.png",
):
    # Read the image
    img = imread(img_path)

    # Try to decode the QR code with the three readers
    qreader_out = qreader_reader.detect_and_decode(image=img)
    cv2_out = cv2_reader.detectAndDecode(img=img)[0]

    print(f"Image: {img_path} -> QReader: {qreader_out}. OpenCV: {cv2_out}.")
