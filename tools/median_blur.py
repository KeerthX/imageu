# tools/median_blur.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class MedianBlurTool(ImageProcessingTool):
    def __init__(self):
        self._kernel_size = 5
        self._validate_kernel_size()

    def _validate_kernel_size(self):
        try:
            if not isinstance(self._kernel_size, int) or self._kernel_size < 1 or self._kernel_size % 2 == 0:
                raise ValueError("Kernel size must be a positive odd integer")
        except Exception as e:
            raise ValueError(f"Invalid kernel size: {str(e)}")

    @property
    def kernel_size(self):
        return self._kernel_size

    @kernel_size.setter
    def kernel_size(self, value):
        self._kernel_size = int(value)
        self._validate_kernel_size()

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            return cv2.medianBlur(image, self._kernel_size)
        except Exception as e:
            raise RuntimeError(f"Error applying median blur: {str(e)}")

    def get_parameters(self):
        return {"kernel_size": self._kernel_size}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "kernel_size" in params:
            self.kernel_size = params["kernel_size"]