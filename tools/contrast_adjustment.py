# tools/contrast_adjustment.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class ContrastAdjustmentTool(ImageProcessingTool):
    def __init__(self):
        self._contrast = 1.0
        self._validate_contrast(self._contrast)

    def _validate_contrast(self, value):
        try:
            value = float(value)
            if value < 0:
                raise ValueError("Contrast factor must be non-negative")
            return value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid contrast value: {str(e)}")

    @property
    def contrast(self):
        return self._contrast

    @contrast.setter
    def contrast(self, value):
        self._contrast = self._validate_contrast(value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            adjusted = cv2.multiply(image, np.array([self._contrast]))
            return np.clip(adjusted, 0, 255).astype(np.uint8)
        except Exception as e:
            raise RuntimeError(f"Error adjusting contrast: {str(e)}")

    def get_parameters(self):
        return {"contrast": self._contrast}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")

        if "contrast" in params:
            self.contrast = params["contrast"]