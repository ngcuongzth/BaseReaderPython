import zxingcpp
from pyzbar.pyzbar import ZBarSymbol, decode as decodeQR
import numpy as np
from core.InitModels import init_wechatqrcode
import cv2
import numpy as np


class PreProcessingImage:
    def __init__(self, is_use_wechat: bool = True):
        self.name = "Preprocessor Image"
        self._SHARPEN_KERNEL = np.array(
            ((-1.0, -1.0, -1.0), (-1.0, 9.0, -1.0), (-1.0, -1.0, -1.0)),
            dtype=np.float32,
        )
        if is_use_wechat:
            self.wechat_qrcode_detector = init_wechatqrcode()

    def optionReadMethod(self, type: int, image: np.ndarray):
        """type decode:\n
        -> 1: use WeChatQRCode\n
        -> 2: use ZxingCpp\n
        -> 3: use Pyzbar\n
        """
        # use wechatqrcode
        if type == 1:
            res, _ = self.wechat_qrcode_detector.detectAndDecode(image)
            if len(res):
                return res[0]
            return None
        elif type == 2:  # zxingcpp
            data_decodeded = zxingcpp.read_barcodes(image)
            if len(data_decodeded) > 0:
                return data_decodeded[0].text
            return None
        elif type == 3:  # pyzbar
            decoded_data = decodeQR(image, symbols=ZBarSymbol)
            if len(decoded_data) > 0:
                return decoded_data[0].data.decode("utf-8")
            return None
        else:
            raise Exception("Truyen vao lua chon khong dung!")

    def __threshold_and_blur_decodings_custom(
        self,
        image: np.ndarray,
        blur_kernel_sizes,
        type: int = 1,
    ):
        assert (
            2 <= len(image.shape) <= 3
        ), f"image must be 2D or 3D (HxW[xC]) (uint8). Got {image.shape}"
        decodedQR = self.optionReadMethod(type=type, image=image)
        if decodedQR is not None:
            return decodedQR
        else:
            # Try to binarize the image (Only works with 2D images)
            if len(image.shape) == 2:
                _, binary_image = cv2.threshold(
                    image,
                    thresh=0,
                    maxval=255,
                    type=cv2.THRESH_BINARY + cv2.THRESH_OTSU,
                )
                decodedQR = self.optionReadMethod(type=type, image=binary_image)
                if decodedQR is not None:
                    return decodedQR

                for kernel_size in blur_kernel_sizes:
                    assert (
                        isinstance(kernel_size, tuple) and len(kernel_size) == 2
                    ), f"kernel_size must be a tuple of 2 elements. Got {kernel_size}"
                    assert all(
                        kernel_size[i] % 2 == 1 for i in range(2)
                    ), f"kernel_size must be a tuple of odd elements. Got {kernel_size}"

                    # If it not works, try to parse to sharpened grayscale
                    blur_image = cv2.GaussianBlur(
                        src=image, ksize=kernel_size, sigmaX=0
                    )
                    decodedQR = self.optionReadMethod(type=type, image=blur_image)
                    if decodedQR is not None:
                        return decodedQR
        return None

    def readQRCodeProcessor(self, image: np.ndarray, type: int = 1):
        """type decode:
        -> 1: use WeChatQRCode
        -> 2: use ZxingCpp
        -> 3: use Pyzbar
        """

        for scale_factor in [1, 1.5]:
            if (
                not all(25 < axis < 1024 for axis in image.shape[:2])
                and scale_factor != 1
            ):
                continue

            rescaled_image = cv2.resize(
                src=image,
                dsize=None,
                fx=scale_factor,
                fy=scale_factor,
                interpolation=cv2.INTER_CUBIC,
            )

            decodeQR = self.optionReadMethod(type=type, image=rescaled_image)
            if decodeQR is not None:
                return decodeQR
            else:
                # For QRs with black background and white foreground, try to invert the image
                inverted_image = image = 255 - rescaled_image
                decodeQR = self.optionReadMethod(type=type, image=inverted_image)
                if decodeQR is not None:
                    return decodeQR
                else:
                    # If it not works, try to parse to grayscale (if it is not already)
                    if len(rescaled_image.shape) == 3:
                        assert (
                            rescaled_image.shape[2] == 3
                        ), f"Image must be RGB or BGR, but it has {image.shape[2]} channels."
                        gray = cv2.cvtColor(rescaled_image, cv2.COLOR_RGB2GRAY)
                    else:
                        gray = rescaled_image
                        decodeQR = self.__threshold_and_blur_decodings_custom(
                            image=gray, blur_kernel_sizes=((5, 5), (7, 7)), type=type
                        )

                        if decodeQR is not None:
                            return decodeQR
                        if len(rescaled_image.shape) == 3:
                            # If it not works, try to sharpen the image
                            sharpened_gray = cv2.cvtColor(
                                cv2.filter2D(
                                    src=rescaled_image,
                                    ddepth=-1,
                                    kernel=self._SHARPEN_KERNEL,
                                ),
                                cv2.COLOR_RGB2GRAY,
                            )
                        else:
                            sharpened_gray = cv2.filter2D(
                                src=rescaled_image,
                                ddepth=-1,
                                kernel=self._SHARPEN_KERNEL,
                            )
                        decodeQR = self.__threshold_and_blur_decodings_custom(
                            image=sharpened_gray, blur_kernel_sizes=((3, 3),)
                        )
                        if decodeQR is not None:
                            return decodeQR
        return None
