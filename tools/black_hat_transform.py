# tools/black_hat_transform_tool.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class BlackHatTransformTool(ImageProcessingTool):
    def __init__(self):
        self._kernel_size = 5
        self._kernel_shape = cv2.MORPH_RECT
        self._validate_parameters(self._kernel_size, self._kernel_shape)

    def _validate_parameters(self, kernel_size, kernel_shape):
        try:
            kernel_size = int(kernel_size)
            if kernel_size <= 0 or kernel_size % 2 == 0:
                raise ValueError("Kernel size must be an odd positive number")
            
            valid_shapes = [cv2.MORPH_RECT, cv2.MORPH_ELLIPSE, cv2.MORPH_CROSS]
            if kernel_shape not in valid_shapes:
                raise ValueError("Invalid kernel shape")
                
            return kernel_size, kernel_shape
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def kernel_size(self):
        return self._kernel_size

    @kernel_size.setter
    def kernel_size(self, value):
        self._kernel_size, _ = self._validate_parameters(value, self._kernel_shape)

    @property
    def kernel_shape(self):
        return self._kernel_shape

    @kernel_shape.setter
    def kernel_shape(self, value):
        _, self._kernel_shape = self._validate_parameters(self._kernel_size, value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
            
        try:
            kernel = cv2.getStructuringElement(self._kernel_shape, 
                                             (self._kernel_size, self._kernel_size))
            return cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)
        except Exception as e:
            raise RuntimeError(f"Error applying black hat transform: {str(e)}")

    def get_parameters(self):
        return {
            "kernel_size": self._kernel_size,
            "kernel_shape": self._kernel_shape
        }

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "kernel_size" in params:
            self.kernel_size = params["kernel_size"]
        if "kernel_shape" in params:
            self.kernel_shape = params["kernel_shape"]