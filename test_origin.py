import cv2
import time
from pyzbar.pyzbar import decode


def readQRCodeProcessor(image):
    # Sử dụng pyzbar để giải mã mã QR từ hình ảnh
    barcodes = decode(image)
    if len(barcodes) > 0:
        return barcodes[0].data.decode("utf-8")
    else:
        return None


# Đọc hình ảnh từ tệp
image_path = "path_to_your_image.png"
image = cv2.imread(image_path)

# Kiểm tra xem hình ảnh có được đọc thành công không
if image is None:
    raise ValueError("Image not loaded correctly. Check the file path or image source.")

# Chuyển đổi hình ảnh sang màu xám
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Khởi tạo bộ đếm và thời gian bắt đầu
count = 0
start_time = time.perf_counter()

# Gọi hàm để đọc mã QR từ hình ảnh màu xám
data_decode = readQRCodeProcessor(gray)

# Tính thời gian xử lý
end_time = time.perf_counter()
elapsed_time = end_time - start_time

# Kiểm tra dữ liệu giải mã và đếm số lần giải mã thành công
if data_decode is None:
    print("No QR code found.")
else:
    count += 1
    print("DATA: ", data_decode)

# In thời gian xử lý
print(
    "Time taken: {:.6f} seconds ({:.3f} ms)".format(elapsed_time, elapsed_time * 1000)
)

# In tổng số lần giải mã thành công
print("Total successful decodes: ", count)

# Hiển thị hình ảnh để xác nhận
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
