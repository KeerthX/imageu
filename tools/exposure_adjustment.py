# tools/exposure_adjustment.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class ExposureAdjustmentTool(ImageProcessingTool):
    def __init__(self):
        self._exposure = 1.0
        self._validate_exposure(self._exposure)

    def _validate_exposure(self, value):
        try:
            value = float(value)
            if value <= 0:
                raise ValueError("Exposure value must be positive")
            return value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid exposure value: {str(e)}")

    @property
    def exposure(self):
        return self._exposure

    @exposure.setter
    def exposure(self, value):
        self._exposure = self._validate_exposure(value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            adjusted = cv2.multiply(image, np.array([self._exposure]))
            return np.clip(adjusted, 0, 255).astype(np.uint8)
        except Exception as e:
            raise RuntimeError(f"Error adjusting exposure: {str(e)}")

    def get_parameters(self):
        return {"exposure": self._exposure}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "exposure" in params:
            self.exposure = params["exposure"]
