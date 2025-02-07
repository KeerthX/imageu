# tools/sobel_filter.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class SobelFilterTool(ImageProcessingTool):
    def __init__(self):
        self._kernel_size = 3
        self._dx = 1
        self._dy = 1
        self._scale = 1.0
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if not isinstance(self._kernel_size, int) or self._kernel_size < 1 or self._kernel_size % 2 == 0:
                raise ValueError("Kernel size must be a positive odd integer")
            if not isinstance(self._dx, int) or self._dx < 0 or self._dx > 2:
                raise ValueError("dx must be 0, 1, or 2")
            if not isinstance(self._dy, int) or self._dy < 0 or self._dy > 2:
                raise ValueError("dy must be 0, 1, or 2")
            if not isinstance(self._scale, (int, float)) or self._scale <= 0:
                raise ValueError("Scale must be positive")
        except Exception as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def parameters(self):
        return {
            "kernel_size": self._kernel_size,
            "dx": self._dx,
            "dy": self._dy,
            "scale": self._scale
        }

    @parameters.setter
    def parameters(self, values):
        if not isinstance(values, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "kernel_size" in values:
            self._kernel_size = int(values["kernel_size"])
        if "dx" in values:
            self._dx = int(values["dx"])
        if "dy" in values:
            self._dy = int(values["dy"])
        if "scale" in values:
            self._scale = float(values["scale"])
        self._validate_parameters()

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            # Convert to grayscale if color image
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Apply Sobel operator
            sobel = cv2.Sobel(
                gray,
                cv2.CV_64F,
                self._dx,
                self._dy,
                ksize=self._kernel_size,
                scale=self._scale
            )
            
            # Convert back to uint8
            abs_sobel = np.absolute(sobel)
            return np.uint8(abs_sobel)
        except Exception as e:
            raise RuntimeError(f"Error applying Sobel filter: {str(e)}")

    def get_parameters(self):
        return self.parameters

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        self.parameters = params
