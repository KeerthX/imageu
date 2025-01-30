# tools/filter_tool.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class FilterTool(ImageProcessingTool):
    def __init__(self):
        self._kernel_size = 5
        self._validate_kernel_size(self._kernel_size)

    def _validate_kernel_size(self, size):
        try:
            size = int(size)
            if size <= 0 or size % 2 == 0:
                raise ValueError("Filter size must be an odd positive number (e.g., 3, 5, 7)")
            return size
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid kernel size: {str(e)}")

    @property
    def kernel_size(self):
        return self._kernel_size

    @kernel_size.setter
    def kernel_size(self, value):
        self._kernel_size = self._validate_kernel_size(value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            return cv2.GaussianBlur(image, (self._kernel_size, self._kernel_size), 0)
        except Exception as e:
            raise RuntimeError(f"Error applying filter: {str(e)}")

    def get_parameters(self):
        return {"kernel_size": self._kernel_size}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "kernel_size" in params:
            self.kernel_size = params["kernel_size"]