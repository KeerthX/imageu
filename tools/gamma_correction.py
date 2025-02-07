# tools/gamma_correction.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class GammaCorrectionTool(ImageProcessingTool):
    def __init__(self):
        self._gamma = 1.0
        self._validate_gamma(self._gamma)

    def _validate_gamma(self, value):
        try:
            value = float(value)
            if value <= 0:
                raise ValueError("Gamma value must be positive")
            return value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid gamma value: {str(e)}")

    @property
    def gamma(self):
        return self._gamma

    @gamma.setter
    def gamma(self, value):
        self._gamma = self._validate_gamma(value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            # Normalize to 0-1 range
            normalized = image.astype(np.float32) / 255.0
            # Apply gamma correction
            corrected = np.power(normalized, 1.0/self._gamma)
            # Convert back to 0-255 range
            return (corrected * 255).astype(np.uint8)
        except Exception as e:
            raise RuntimeError(f"Error applying gamma correction: {str(e)}")

    def get_parameters(self):
        return {"gamma": self._gamma}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "gamma" in params:
            self.gamma = params["gamma"]