# [Github Repository - BaseReader](https://github.com/ngcuongzth/BaseReaderPython.git)

![](https://media.giphy.com/media/xT5LMywOTMWtK7iqSA/giphy.gif?cid=790b7611jqczv8h4ese9klj0b8hlm7km9u19ph8ottb9lhp7&ep=v1_gifs_search&rid=giphy.gif&ct=g)

## BaseReader 
- Sử dụng với mục đích xây dựng base chung cho dự án đọc mã (Datamatrix, QRCode, Barcode)
- Các thư viện được sử dụng đọc mã:
    
    - **qreader**: là giải pháp để đọc các mã QR Code khó, sử dụng Yolo [https://pypi.org/project/qreader]
    
    - **zxingcpp**: [https://pypi.org/project/zxing-cpp]

    - **pyzbar**: [https://pypi.org/project/pyzbar]

    - **pylibdmtx**: [https://pypi.org/project/pylibdmtx]


    ![][def]



### Hỗ trợ các hàm tiện ích xử lý ảnh:
    
### `core/ImageProcessor.py`: `class xử lý ảnh`
    
#### Làm việc với đọc, ghi, hiển thị ảnh

- **showImage**: Hiển thị ảnh 
- **saveImage**: Lưu ảnh
- **readImage**: Đọc ảnh 
- **readAndConvertToGray**: Đọc và chuyển về gray 

#### Thay đổi hình thái ảnh
    
- **resizeImage**: thay đổi kích thước ảnh 
- **cropImage**: cắt ảnh
- **rotateImage**: xoay ảnh
- **useRoiImage**: Cắt ảnh theo tọa độ và trả về ảnh được cắt 

#### Lấy thông tin ảnh

- **getSizeImage**: lấy kích thước của ảnh (dài, rộng)
- **isBinaryImage**: kiểm tra xem có là ảnh đen trắng không

#### Làm mịn, làm mờ ảnh

- **blurImage**: làm mờ với hàm `blur`
- **blurGaussianImage**: làm mờ với thuật toán `Gaussian`
- **medianBlurImage**: làm mờ với thuật toán `medianBlur`

#### Cải thiện, xử lý ảnh
- **useSuperResolution**: Cải thiện chi tiết ảnh 
- **automatic_brightness_and_contrast**: Cân bằng sáng, tương phản ảnh
- **useErosion**: kỹ thuật ăn mòn ảnh
- **useDilation**: kỹ thuật giãn nở ảnh 
- **useOpening**: kỹ thuật kết hợp ăn mòn (1) và giãn nở (2)
- **useClosing**: kỹ thuật kết hợp ăn mòn (2) và giãn nở (1)
- **useThreshBinary**: sử dụng `ThreshBinary` và `ThreshBinaryINV`

#### Tìm viền và các hàm khác
- **useGradientSolbelX, useGradientSolbelY**
- **useGradientLaplacian**
- **useCannyEdge**
- **ultilities function: order_points, four_point_transform, contours_warped**
- **templateMatching**: kỹ thuật template matching ảnh


### Giải mã mã vạch
![][def2]
> ### *Nên xử lý ảnh trước khi đưa vào hàm đọc mã*

Ví dụ về sử dụng `useQreader`

`core/BarcodeProcessor.py`: `class đọc mã Barcode`:
#### Sử dụng
    Từ file chính, hãy import và tạo đối tượng với class BarcodeProcessor, ví dụ đọc mã bằng `zxingcpp`:
    

```python
    from core.ImageProcessor import ImageProcessor
    from core.BarcodeProcessor import BarcodeProcessor

    Processor = ImageProcessor(is_init_dnn_superres=True) 
    #is_init_dnn_superes: có sử dụng Super Resolution hay không? mặc định là True
    Reader = BarcodeProcessor()
    # read image
    image = Processor.readImage("./images/barcode/barcode.png")
    # process with super solution (option)
    image_processed = Processor.useSuperResolution(image)
    data_decoded = Reader.useZxingCpp(image_processed)
    print("data:", data_decoded)  # output: ->  data: SD Team`
```


- **useZxingCpp**: đọc mã bằng `zxingcpp`
- **usePyzbar**: đọc mã bằng `pyzbar`
- **useLoopReader**: đọc mã bằng hàm loop các thư viện (`custom`)

`core/DatamatrixProcessor.py`: `class đọc mã Datamatrix`
#### Sử dụng

```python
    from core.ImageProcessor import ImageProcessor
    from core.DatamatrixProcessor import DatamatrixProcessor

    Processor = ImageProcessor(is_init_dnn_superres=True)
    Reader = DatamatrixProcessor()
    # read image
    image = Processor.readImage("./images/datamatrix/datamatrix.png")
    # process with super solution (option)
    image_processed = Processor.useSuperResolution(image)
    data_decoded = Reader.usePylibdmtx(image_processed)
    print("data:", data_decoded)  # output: ->  data: SD Team
```


- **usePylibdmtx**: đọc mã bằng `pylibdmtx`
- **useZxingcpp**: đọc mã bằng `useZxingcpp`
- **useLoopReader**: đọc mã bằng hàm loop các thư viện (`custom`)

`core/QRCodeProcessor.py`: `class đọc mã QRCode`

Ví dụ sử dụng qreader

```python
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
```

![][def]

### `Nhận xét chung:` `useQreader()` cho trải khả năng đọc mã tốt hơn so với thư viện khác, đổi lại tốc độ của nó chậm hơn `~0.2s` thay vì `< 0.1s` như các thư viện khác, tùy dự án chúng ta sẽ phải `custom` lại

- **useQReader**: đọc mã bằng `qreader`
- **useWeChatQRCode**: đọc mã bằng `WechatQRCode`
- **usePyzbar**: đọc mã bằng `pyzbar`
- **useZxingCpp**: đọc mã bằng `useZxingCpp`
- **useLoopReader**: đọc mã với hàm loop (`custom`)



[def]: https://media.giphy.com/media/v1.Y2lkPTc5MGINjExNG1ncG1pZWt1YTBxdXVjMWtydTJmcTkyb2Mxa2h6aWQ4MWhnOHp5YSZlcD12MV9naWZzXNlYXJjaCZjdD1n/4pMX5rJ4PYAEM/giphy.gif
[def2]: https://media.giphy.com/media/lq2K5jinAlChoCLS/giphy.gif?cid=82a149bqchjujr870tnynfa7bvsqci9mmldyfowzglma49&ep=v1_gifs_trending&rid=giphy.gif&ct=g
[def]: https://media.giphy.com/media/v1.Y2lkPTc5MGINjExaXBkYzJydDVsYXlscW5lMnUycTRzdlwY252cjl2NjJ2NXlhYzRsMSZlcD12MV9naWZzXNlYXJjaCZjdD1n/o8doT9BL7dgtolp7O/giphy.gif
