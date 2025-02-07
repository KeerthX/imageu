# tools/saturation_adjustment.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class SaturationAdjustmentTool(ImageProcessingTool):
    def __init__(self):
        self._saturation = 1.0
        self._validate_saturation(self._saturation)

    def _validate_saturation(self, value):
        try:
            value = float(value)
            if value < 0:
                raise ValueError("Saturation value must be non-negative")
            return value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid saturation value: {str(e)}")

    @property
    def saturation(self):
        return self._saturation

    @saturation.setter
    def saturation(self, value):
        self._saturation = self._validate_saturation(value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
            hsv[:, :, 1] *= self._saturation
            hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
            return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        except Exception as e:
            raise RuntimeError(f"Error adjusting saturation: {str(e)}")

    def get_parameters(self):
        return {"saturation": self._saturation}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "saturation" in params:
            self.saturation = params["saturation"]