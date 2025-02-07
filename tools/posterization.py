# tools/posterization.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class PosterizationTool(ImageProcessingTool):
    def __init__(self):
        self._levels = 4
        self._validate_levels(self._levels)

    def _validate_levels(self, value):
        try:
            value = int(value)
            if value < 2 or value > 8:
                raise ValueError("Posterization levels must be between 2 and 8")
            return value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid levels value: {str(e)}")

    @property
    def levels(self):
        return self._levels

    @levels.setter
    def levels(self, value):
        self._levels = self._validate_levels(value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            # Calculate the division factor based on levels
            factor = 255 / (self._levels - 1)
            # Quantize the image
            quantized = np.round(image / factor) * factor
            return quantized.astype(np.uint8)
        except Exception as e:
            raise RuntimeError(f"Error applying posterization: {str(e)}")

    def get_parameters(self):
        return {"levels": self._levels}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "levels" in params:
            self.levels = params["levels"]
