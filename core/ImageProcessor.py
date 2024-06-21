"""
Image Processor
@repository: `https://github.com/ngcuongzth/BaseReaderPython`
@document&libs: OpenCV
@last&update: 2024/06/20
"""

import cv2
from core.InitModels import init_dnn_superres
import numpy as np
from PIL import Image
import imutils


class ImageProcessor:
    def __init__(self, is_init_dnn_superres=True):

        if is_init_dnn_superres:
            self.superres = init_dnn_superres()
            self.is_init_dnn_superres = True
        else:
            self.is_init_dnn_superres = False

    def useSuperResolution(self, image: np.ndarray):
        """Cai thien chi tiet anh"""

        if self.is_init_dnn_superres:
            image = self.superres.upsample(image)
            # blur = cv2.medianBlur(image, (blurSize))
            return image
        else:
            raise Exception("is_init_dnn_superres ? --- just-ngcuong")

    def automatic_brightness_and_contrast(self, image, clip_hist_percent=1):
        """ "tu dong chinh sang/tuong phan anh
        @return : tupple(image_result, alpha_value, beta_value)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Calculate grayscale histogram
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_size = len(hist)
        # Calculate cumulative distribution from the histogram
        accumulator = []
        accumulator.append(float(hist[0]))
        for index in range(1, hist_size):
            accumulator.append(accumulator[index - 1] + float(hist[index]))
        # Locate points to clip
        maximum = accumulator[-1]
        clip_hist_percent *= maximum / 100.0
        clip_hist_percent /= 2.0
        # Locate left cut
        minimum_gray = 0
        while accumulator[minimum_gray] < clip_hist_percent:
            minimum_gray += 1
        # Locate right cut
        maximum_gray = hist_size - 1
        while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
            maximum_gray -= 1
        # Calculate alpha and beta values
        alpha = 255 / (maximum_gray - minimum_gray)
        beta = -minimum_gray * alpha
        auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

        return (auto_result, alpha, beta)

    def useRoiImage(self, image: np.ndarray, rect: np.array, gap: int):
        """ "cat anh theo toa do truyen vao va tra ve anh moi + 10px"""
        x = rect[0] - gap
        y = rect[1] - gap
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        roi = image[y : y + rect[3] + gap, x : x + rect[2] + gap]
        return roi

    # ! Start OS File
    def readImage(self, path: str):
        """read image"""
        return cv2.imread(path)

    def readAndConvertToGray(self, path: str):
        """read and convert iamge to grayscale"""
        if path:
            image = Image.open(path)
            gray_image = image.convert("L")
        else:
            gray_image = image.convert("L")
        return gray_image

    def convertToGrayscale(self, image: np.ndarray):
        """convert image to grayscale"""
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def showImage(self, window_name: str, image: np.ndarray, waitKey: int = 0):
        """show image"""
        cv2.imshow(window_name, image)
        cv2.waitKey(waitKey)

    def saveImage(self, path_save: str, image: np.ndarray):
        """save image"""
        cv2.imwrite(filename=path_save, img=image)

    #!  Geometric Transformations of Images

    def resizeImage(self, image, sizeScale: float, isZoom: bool = True):
        "resize image"
        if isZoom:
            image = cv2.resize(
                image, None, fx=sizeScale, fy=sizeScale, interpolation=cv2.INTER_CUBIC
            )
        else:
            image = cv2.resize(
                image, None, fx=sizeScale, fy=sizeScale, interpolation=cv2.INTER_LINEAR
            )
        return image

    def cropImage(self, image, rect: tuple):
        # rect : (x1,x2,y1,y2)
        x1, x2, y1, y2 = rect
        if len(rect) != 4:
            raise Exception("Need pass enough 4 points of rect (x1,x2,y1,y2)")
        else:
            crop = image[x1:x2, y1:y2]
            return crop

    def rotateImage(self, image: np.ndarray, angle: int, scaleSize: float = 1.0):
        "rotate"
        h, w = self.getSizeImage(image)

        center = (w // 2, h // 2)
        maxtrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=scaleSize)
        rotatedImage = cv2.warpAffine(image, maxtrix, (w, h))
        return rotatedImage

    def getSizeImage(self, image: np.ndarray):
        """ "get size image
        @ return a tupple (h,w)
        """
        h, w = image.shape[:2]
        return w, h

    # !  Morphological Transformations

    def isBinaryImage(self, image: np.ndarray):
        """@ output: boolean value"""
        is_binary = image.min() == 0 and image.max() == 255

        if is_binary:
            return True
        else:
            return False

    def useErosion(
        self, image: np.ndarray, kernel: tuple = (3, 3), iterations: int = 1
    ):
        """
        @ ăn mòn
        - Làm giảm kích thước của các đối tượng trắng và loại bỏ các đặc điểm nhỏ,
        nhưng giữ nguyên các đường viền và hình dạng chính của đối tượng

        @arguments
        `image`: ảnh đầu vào
        `kernel`: ma trận vùng cần xói mòn
        `iterations`: số lần thực hiện

        @ output: image result
        """
        if self.isBinaryImage(image) == False:
            image = self.convertToGrayscale(image)
        kernel = np.ones(kernel, np.uint8)

        erosion = cv2.erode(image, kernel=kernel, iterations=iterations)
        return erosion

    def useDilation(self, image, kernel: tuple = (3, 3), iterations=1):
        """
        @ giãn nở:
        - Tăng kích thước của các đối tượng trắng, làm kết nối các đối tượng gần nhau và lấp đầy các lỗ hổng

        @arguments
        `image`: ảnh đầu vào
        `kernel` : ma trận vùng được mở rộng
        `iterations`: số lần thực hiện

        @ output: image result
        """

        if self.isBinaryImage(image) == False:
            image = self.convertToGrayscale(image)
        kernel = np.ones(kernel, np.uint8)
        dilation = cv2.dilate(image, kernel=kernel, iterations=iterations)
        return dilation

    def useOpening(self, image: np.ndarray, kernel: tuple = (3, 3)):
        """
        `erosion -> dilation`
        @ - Kết hợp phép ăn mòn và giãn nở theo trình tự:
                        `ăn mòn trước`, sau đó `giãn nở`.
        - Loại bỏ các đối tượng nhỏ và các chi tiết không mong muốn trong hình ảnh, giữ lại các cạnh và hình dạng chính của các vùng đối tượng lớn hơn.

        @argument:
        `kernel`: ma trận kích thước
        `image`: image input

        @output: image result
        """

        if self.isBinaryImage(image) == False:
            image = self.convertToGrayscale(image)

        kernel = np.ones(kernel, np.uint8)
        opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel=kernel)
        return opening

    def useClosing(self, image: np.ndarray, kernel: tuple = (3, 3)):
        """
        `dilation -> erosion`
        - Kết hợp phép giãn nở và ăn mòn theo trình tự:
                    `giãn nở trước, sau đó ăn mòn.`
        - Loại bỏ các lỗ hổng nhỏ và kết nối các đối tượng gần nhau trong hình ảnh, giữ lại các đường viền và hình dạng chính của các đối tượng.

        """

        if self.isBinaryImage(image) == False:
            image = self.convertToGrayscale(image)

        kernel = np.ones(kernel, np.uint8)

        closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel=kernel)
        return closing

    #!  Thresholding

    def useThreshBinary(
        self,
        image: np.ndarray,
        minThresh: int = 0,
        maxThresh: int = 255,
        typeThresh: int = 1,
    ):
        """convert image to thresh binary image"""

        if minThresh >= maxThresh:
            raise Exception(
                "The value of `minThresh` must be less than `maxThresh` - just.ngcuong"
            )

        if minThresh > 255 or maxThresh > 255:
            raise Exception(
                "The value of `thresh` must be less than <= 255 - just.ngcuong"
            )

        if typeThresh != 1 and typeThresh != -1:
            raise Exception("Pass in the value -1 or 1.  - just.ngcuong")

        else:
            if self.isBinaryImage(image) == False:
                image = self.convertToGrayscale(image)

            if typeThresh == 1:
                ret, thresh = cv2.threshold(
                    image, minThresh, maxThresh, cv2.THRESH_BINARY
                )
            else:
                ret, thresh = cv2.threshold(
                    image, minThresh, maxThresh, cv2.THRESH_BINARY_INV
                )

        return thresh

    #! Blur Smooth

    def blurImage(self, image: np.ndarray, kernel: tuple = (3, 3)):
        blur = cv2.blur(image, kernel)
        return blur

    def blurGaussianImage(
        self, image: np.ndarray, kernel: tuple = (3, 3), sigmaX: int = 0
    ):
        blur = cv2.GaussianBlur(image, kernel, sigmaX)
        return blur

    def medianBlurImage(self, image: np.ndarray, kernel: tuple = (3, 3)):
        blur = cv2.medianBlur(image, kernel)
        return blur

    #! Gradient
    def useGradientSolbelX(self, image: np.ndarray, depth, ksize: int = 3):
        if self.isBinaryImage(image) == False:
            image = self.convertToGrayscale(image)
        image = cv2.Sobel(image, depth, 1, 0, ksize=ksize)
        return image

    def useGradientSolbelY(self, image: np.ndarray, depth, ksize: int = 3):
        if self.isBinaryImage(image) == False:
            image = self.convertToGrayscale(image)
        image = cv2.Sobel(image, depth, 0, 1, ksize=ksize)
        return image

    def useGradientLaplacian(self, image: np.ndarray):
        if self.isBinaryImage(image) == False:
            image = self.convertToGrayscale(image)
        image = cv2.Laplacian(image, cv2.CV_64F)
        return image

    #! Canny Edge Detection
    def useCannyEdge(self, image: np.ndarray, minThresh: int = 0, maxThresh: int = 255):
        if minThresh >= maxThresh:
            raise Exception(
                "The value of `minThresh` must be less than `maxThresh` - just.ngcuong"
            )
        if minThresh > 255 or maxThresh > 255:
            raise Exception(
                "The value of `thresh` must be less than <= 255 - just.ngcuong"
            )
        edges_image = cv2.Canny(image, minThresh, maxThresh)
        return edges_image

    #! Contours

    def order_points(self, pts):
        """
        nhận vào 1 list `pts` gồm 4 điểm và sắp xếp chúng theo thứ tự cụ thể để xây dựng một hình chữ nhật

        @output: trả về tọa độ (tl,tr,br,bl)
        """
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    def four_point_transform(self, image, pts):
        rect = self.order_points(pts)
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        dst = np.array(
            [
                [10, 10],
                [maxWidth - 10, 10],
                [maxWidth - 10, maxHeight - 10],
                [10, maxHeight - 10],
            ],
            dtype="float32",
        )
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        return warped

    def contours_warped(self, gray, roi_warped):
        ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
        gradX = self.useGradientSolbelX(gray, depth=ddepth, ksize=-1)
        gradY = self.useGradientSolbelY(gray, depth=ddepth, ksize=-1)
        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)
        blurred = self.blurImage(gradient, kernel=9)
        thresh = self.useThreshBinary(
            blurred, minThresh=160, maxThresh=255, typeThresh=1
        )
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
        closed = self.useClosing(thresh, kernel=kernel)
        erode = self.useErosion(closed, kernel=(1, 1), iterations=4)
        dilate = self.useDilation(erode, kernel=(1, 1), iterations=4)

        contours, hierarchy = cv2.findContours(
            dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
        )
        for i in contours:
            x, y, w, h = cv2.boundingRect(i)
            rect = cv2.minAreaRect(i)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            pts = np.array(box, dtype="float32")
            # condition here
            if (55 < h < 165) and (240 < w < 300):
                # print(h, w)
                roi = roi_warped[y : y + h, x : x + w].copy()
                roi_warped = self.four_point_transform(roi_warped, pts)
        return roi_warped

    def templateMatching(
        self,
        image: np.ndarray,
        template: np.ndarray,
        threshold: float = 0.6,
        is_show: bool = False,
    ):
        if threshold <= 0 or threshold > 1:
            return Exception(" 0 < threshold <= 1   --- just.ngcuong")
        w, h = self.getSizeImage(template)
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            x1, y1 = max_loc
            x2, y2 = x1 + w, y1 + h
            if is_show:
                self.showImage("image", image)
                self.showImage("template", template)
                image_show = image.copy()
                cv2.rectangle(image_show, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.imshow("Detected", image_show)
                cv2.waitKey(0)
            return x1, y1, x2, y2
        else:
            return None
