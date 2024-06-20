"""
This class the YOLOv7 QR Detector. It uses a YOLOv7-tiny model trained to detect QR codes in the wild.

Author: Eric Canas.
Github: https://github.com/Eric-Canas/qrdet
Email: eric@ericcanas.com
Date: 11-12-2022
Custom: just.ngcuong
Github: nguyencuongzth/just.ngcuong
"""

from __future__ import annotations
import os

import numpy as np
from ultralytics import YOLO
from qrdet import _yolo_v8_results_to_dict, _prepare_input, BBOX_XYXY, CONFIDENCE
import time

_WEIGHTS_FOLDER = os.path.join(os.path.dirname(__file__), ".model")
_MODEL_FILE_NAME = "qrdet-{size}.pt"


class QRDetector:
    def __init__(
        self, model_size: str = "s", conf_th: float = 0.5, nms_iou: float = 0.3
    ):
        """
        Initialize the QRDetector.
        It loads the weights of the YOLOv8 model and prepares it for inference.
        :param model_size: str. The size of the model to use. It can be 'n' (nano), 's' (small), 'm' (medium) or
                                'l' (large). Larger models are more accurate but slower. Default (and recommended): 's'.
        :param conf_th: float. The confidence threshold to use for the detections. Detection with a confidence lower
                                than this value will be discarded. Default: 0.5.
        :param nms_iou: float. The IoU threshold to use for the Non-Maximum Suppression. Detections with an IoU higher
                                than this value will be discarded. Default: 0.3.
        """
        assert model_size in ("n", "s", "m", "l"), (
            f"Invalid model size: {model_size}. "
            f"Valid values are: 'n', 's', 'm' or 'l'."
        )
        self._model_size = model_size
        path = r"./models/qrdet/qrdet-n.pt"
        # path = self.__download_weights_or_return_path(model_size=model_size)
        # path = r"./models/qrdet/qrdet-n.pt"

        assert os.path.exists(path), f"Could not find model weights at {path}."

        self.model = YOLO(model=path, task="segment")

        self._conf_th = conf_th
        self._nms_iou = nms_iou

    def detect(
        self,
        image: np.ndarray | "PIL.Image" | "torch.Tensor" | str,
        is_bgr: bool = False,
        **kwargs,
    ) -> tuple[dict[str, np.ndarray | float | tuple[float, float]]]:
        """
        Detect QR codes in the given image.

        :param image: str|np.ndarray|PIL.Image|torch.Tensor. Numpy array (H, W, 3), Tensor (1, 3, H, W), or
                                            path/url to the image to predict. 'screen' for grabbing a screenshot.
        :param legacy: bool. If sent as **kwarg**, will parse the output to make it identical to 1.x versions.
                            Not Recommended. Default: False.
        :return: tuple[dict[str, np.ndarray|float|tuple[float, float]]]. A tuple of dictionaries containing the
            following keys:
            - 'confidence': float. The confidence of the detection.
            - 'bbox_xyxy': np.ndarray. The bounding box of the detection in the format [x1, y1, x2, y2].
            - 'cxcy': tuple[float, float]. The center of the bounding box in the format (x, y).
            - 'wh': tuple[float, float]. The width and height of the bounding box in the format (w, h).
            - 'polygon_xy': np.ndarray. The accurate polygon that surrounds the QR code, with shape (N, 2).
            - 'quadrilateral_xy': np.ndarray. The quadrilateral that surrounds the QR code, with shape (4, 2).
            - 'expanded_quadrilateral_xy': np.ndarray. An expanded version of quadrilateral_xy, with shape (4, 2),
                that always include all the points within polygon_xy.

            All these keys (except 'confidence') have a 'n' (normalized) version. For example, 'bbox_xyxy' is the
            bounding box in absolute coordinates, while 'bbox_xyxyn' is the bounding box in normalized coordinates
            (from 0. to 1.).
        """

        image = _prepare_input(source=image, is_bgr=is_bgr)
        # Predict

        # print("start")
        # stime = time.time()

        results = self.model.predict(
            source=image,
            conf=self._conf_th,
            iou=self._nms_iou,
            half=False,
            device=None,
            max_det=100,
            augment=False,
            agnostic_nms=True,
            classes=None,
            verbose=False,
        )
        assert (
            len(results) == 1
        ), f"Expected 1 result if no batch sent, got {len(results)}"

        # print("end")
        # print(time.time() - stime)

        # print("start yolooooooooo", time.time() - stime)
        results = _yolo_v8_results_to_dict(results=results[0], image=image)
        # results = _yolo_v8_results_to_dict(results=[], image=image)

        # print("doneeeeee yolooooooooo", time.time() - stime)

        if "legacy" in kwargs and kwargs["legacy"]:
            return self._parse_legacy_results(results=results, **kwargs)

        # print("doneeeeeeee detecttttttttttt", time.time() - stime)

        return results

    def _parse_legacy_results(
        self, results, return_confidences: bool = True, **kwargs
    ) -> (
        tuple[tuple[list[float, float, float, float], float], ...]
        | tuple[list[float, float, float, float], ...]
    ):
        """
        Parse the results to make it compatible with the legacy version of the library.
        :param results: tuple[dict[str, np.ndarray|float|tuple[float, float]]]. The results to parse.
        """
        if return_confidences:
            return tuple((result[BBOX_XYXY], result[CONFIDENCE]) for result in results)
        else:
            return tuple(result[BBOX_XYXY] for result in results)

    def __del__(self):
        path = os.path.join(
            _WEIGHTS_FOLDER, _MODEL_FILE_NAME.format(size=self._model_size)
        )
        # If the weights didn't finish downloading, delete them.
        if (
            hasattr(self, "downloading_model")
            and self.downloading_model
            and os.path.isfile(path)
        ):
            os.remove(path)
