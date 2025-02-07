# tools/adaptive_threshold_tool.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class AdaptiveThresholdTool(ImageProcessingTool):
    def __init__(self):
        self._max_value = 255
        self._block_size = 11
        self._c = 2
        self._adaptive_method = cv2.ADAPTIVE_THRESH_MEAN_C
        self._threshold_type = cv2.THRESH_BINARY
        self._validate_parameters(self._block_size, self._c, self._max_value)

    def _validate_parameters(self, block_size, c, max_value):
        try:
            block_size = int(block_size)
            c = int(c)
            max_value = int(max_value)
            
            if block_size <= 1 or block_size % 2 == 0:
                raise ValueError("Block size must be an odd number greater than 1")
            if not 0 <= max_value <= 255:
                raise ValueError("Max value must be between 0 and 255")
                
            return block_size, c, max_value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def block_size(self):
        return self._block_size

    @block_size.setter
    def block_size(self, value):
        self._block_size, _, _ = self._validate_parameters(value, self._c, self._max_value)

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        _, self._c, _ = self._validate_parameters(self._block_size, value, self._max_value)

    @property
    def max_value(self):
        return self._max_value

    @max_value.setter
    def max_value(self, value):
        _, _, self._max_value = self._validate_parameters(self._block_size, self._c, value)

    @property
    def adaptive_method(self):
        return self._adaptive_method

    @adaptive_method.setter
    def adaptive_method(self, value):
        valid_methods = [cv2.ADAPTIVE_THRESH_MEAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C]
        if value not in valid_methods:
            raise ValueError("Invalid adaptive method")
        self._adaptive_method = value

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
            
        try:
            # Convert to grayscale if needed
            if len(image.shape) > 2:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            return cv2.adaptiveThreshold(gray, self._max_value, self._adaptive_method,
                                       self._threshold_type, self._block_size, self._c)
        except Exception as e:
            raise RuntimeError(f"Error applying adaptive threshold: {str(e)}")

    def get_parameters(self):
        return {
            "max_value": self._max_value,
            "block_size": self._block_size,
            "c": self._c,
            "adaptive_method": self._adaptive_method,
            "threshold_type": self._threshold_type
        }

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "max_value" in params:
            self.max_value = params["max_value"]
        if "block_size" in params:
            self.block_size = params["block_size"]
        if "c" in params:
            self.c = params["c"]
        if "adaptive_method" in params:
            self.adaptive_method = params["adaptive_method"]