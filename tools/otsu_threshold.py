# tools/otsu_threshold_tool.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class OtsuThresholdTool(ImageProcessingTool):
    def __init__(self):
        self._max_value = 255
        self._validate_max_value(self._max_value)

    def _validate_max_value(self, value):
        try:
            value = int(value)
            if not 0 <= value <= 255:
                raise ValueError("Max value must be between 0 and 255")
            return value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid max value: {str(e)}")

    @property
    def max_value(self):
        return self._max_value

    @max_value.setter
    def max_value(self, value):
        self._max_value = self._validate_max_value(value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
            
        try:
            if len(image.shape) > 2:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            _, thresh = cv2.threshold(gray, 0, self._max_value, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return thresh
        except Exception as e:
            raise RuntimeError(f"Error applying Otsu's threshold: {str(e)}")

    def get_parameters(self):
        return {"max_value": self._max_value}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "max_value" in params:
            self.max_value = params["max_value"]
