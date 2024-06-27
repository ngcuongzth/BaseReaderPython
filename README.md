# [Github Repository - BaseReader](https://github.com/ngcuongzth/BaseReaderPython.git)
## `date release:2024/06/22`

![][def3]

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



`core/PreprocessorDecode.py.py`: `class đọc mã - sử dụng hàm tiền xử lý ảnh của Qreader (custom) + thư viện đọc mã`

- **readQRCodeProcessor(`image`, `type`)**: hàm đọc mã `QRCode`, tham số đầu vào
    `image`: hình ảnh
    `type`: thư viện được sử dụng với giá trị (`1-3`):
    
        `1`: sử dụng thư viện `WeChat`

        `2`: sử dụng thư viện `Zxingcpp`

        `3`: sử dụng thư viện `Pyzbar`



![][def4]

### `Nhận xét chung:`  

- **useQReader**: đọc mã bằng `qreader` (vừa detect, vừa decode - tốc độ ~ 0.2s)
- **useWeChatQRCode**: đọc mã bằng `WechatQRCode` (hàm đọc mã thường)
- **usePyzbar**: đọc mã bằng `pyzbar` (hàm đọc mã thường)
- **useZxingCpp**: đọc mã bằng `useZxingCpp`  (hàm đọc mã thường)
- **useLoopReader**: đọc mã với hàm loop (`custom`) 
- **getRectQReader**: lấy tọa độ của qrcode trong ảnh `(x1,y1,x2,y2)`
- **useQReaderProcessorDecode**: đọc mã với hàm xử lý ảnh của `qreader`
        
    **input**:
        + `image`: một ảnh đầu vào (recommend: ảnh đã crop)
        + `type`: giá trị từ ` 1 đến 3 ` với 
            
    
    + `1`: đọc bằng `WechatQRCode`
    
    + `2`: đọc bằng `Zxingcpp`
    
    + `3`: đọc bằng `Pyzbar`

    **output**: mã được `decode`


[def]: https://media.giphy.com/media/v1.Y2lkPTc5MGINjExNG1ncG1pZWt1YTBxdXVjMWtydTJmcTkyb2Mxa2h6aWQ4MWhnOHp5YSZlcD12MV9naWZzXNlYXJjaCZjdD1n/4pMX5rJ4PYAEM/giphy.gif
[def2]: https://media.giphy.com/media/Um3ljJl8jrnHy/giphy.gif?cid=790b7611njge3hnmfbejhl6o2dqr9a3ll8v3i9sktx9qbkgg&ep=v1_gifs_search&rid=giphy.gif&ct=g

[def]: https://media.giphy.com/media/v1.Y2lkPTc5MGINjExaXBkYzJydDVsYXlscW5lMnUycTRzdlwY252cjl2NjJ2NXlhYzRsMSZlcD12MV9naWZzXNlYXJjaCZjdD1n/o8doT9BL7dgtolp7O/giphy.gif

[def4]: https://media.giphy.com/media/JRE3AvLsSRXg360F6l/giphy.gif?cid=790b7611njge3hnmfbejhl6o2dqr9a3ll8v3i9sktx9qbkgg&ep=v1_gifs_search&rid=giphy.gif&ct=g
[def3]: https://media.giphy.com/media/YFkpsHWCsNUUo/giphy.gif?cid=790b76112rxv4oztdntme277p6md8743qrnzoqvgaaiaydmd&ep=v1_gifs_search&rid=giphy.gif&ct=g




