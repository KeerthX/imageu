# tools/hue_adjustment.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class HueAdjustmentTool(ImageProcessingTool):
    def __init__(self):
        self._hue_shift = 0
        self._validate_hue_shift(self._hue_shift)

    def _validate_hue_shift(self, value):
        try:
            value = int(value)
            if value < -180 or value > 180:
                raise ValueError("Hue shift must be between -180 and 180 degrees")
            return value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid hue shift value: {str(e)}")

    @property
    def hue_shift(self):
        return self._hue_shift

    @hue_shift.setter
    def hue_shift(self, value):
        self._hue_shift = self._validate_hue_shift(value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hsv[:, :, 0] = (hsv[:, :, 0] + self._hue_shift) % 180
            return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        except Exception as e:
            raise RuntimeError(f"Error adjusting hue: {str(e)}")

    def get_parameters(self):
        return {"hue_shift": self._hue_shift}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "hue_shift" in params:
            self.hue_shift = params["hue_shift"]