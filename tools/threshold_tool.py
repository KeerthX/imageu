# tools/threshold_tool.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class SimpleThresholdTool(ImageProcessingTool):
    def __init__(self):
        self._threshold = 127
        self._max_value = 255
        self._threshold_type = cv2.THRESH_BINARY
        self._validate_parameters(self._threshold, self._max_value)

    def _validate_parameters(self, threshold, max_value):
        try:
            threshold = int(threshold)
            max_value = int(max_value)
            
            if not 0 <= threshold <= 255:
                raise ValueError("Threshold must be between 0 and 255")
            if not 0 <= max_value <= 255:
                raise ValueError("Max value must be between 0 and 255")
                
            return threshold, max_value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold, _ = self._validate_parameters(value, self._max_value)

    @property
    def max_value(self):
        return self._max_value

    @max_value.setter
    def max_value(self, value):
        _, self._max_value = self._validate_parameters(self._threshold, value)

    @property
    def threshold_type(self):
        return self._threshold_type

    @threshold_type.setter
    def threshold_type(self, value):
        valid_types = [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV, 
                      cv2.THRESH_TRUNC, cv2.THRESH_TOZERO, cv2.THRESH_TOZERO_INV]
        if value not in valid_types:
            raise ValueError("Invalid threshold type")
        self._threshold_type = value

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
            
        try:
            # Convert to grayscale if needed
            if len(image.shape) > 2:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            _, thresh = cv2.threshold(gray, self._threshold, self._max_value, 
                                    self._threshold_type)
            return thresh
        except Exception as e:
            raise RuntimeError(f"Error applying threshold: {str(e)}")

    def get_parameters(self):
        return {
            "threshold": self._threshold,
            "max_value": self._max_value,
            "threshold_type": self._threshold_type
        }

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "threshold" in params:
            self.threshold = params["threshold"]
        if "max_value" in params:
            self.max_value = params["max_value"]
        if "threshold_type" in params:
            self.threshold_type = params["threshold_type"]

