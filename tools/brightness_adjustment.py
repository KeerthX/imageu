# tools/brightness_adjustment.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class BrightnessAdjustmentTool(ImageProcessingTool):
    def __init__(self):
        self._brightness = 0
        self._validate_brightness(self._brightness)

    def _validate_brightness(self, value):
        try:
            value = float(value)
            if value < -255 or value > 255:
                raise ValueError("Brightness adjustment must be between -255 and 255")
            return value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid brightness value: {str(e)}")

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = self._validate_brightness(value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            adjusted = cv2.add(image, np.full(image.shape, self._brightness, dtype=np.float32))
            return np.clip(adjusted, 0, 255).astype(np.uint8)
        except Exception as e:
            raise RuntimeError(f"Error adjusting brightness: {str(e)}")

    def get_parameters(self):
        return {"brightness": self._brightness}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")

        if "brightness" in params:
            self.brightness = params["brightness"]
