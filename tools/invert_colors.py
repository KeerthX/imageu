# tools/invert_colors.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class InvertColorsTool(ImageProcessingTool):
    def __init__(self):
        self._strength = 1.0
        self._validate_strength(self._strength)

    def _validate_strength(self, value):
        try:
            value = float(value)
            if value < 0.0 or value > 1.0:
                raise ValueError("Inversion strength must be between 0.0 and 1.0")
            return value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid strength value: {str(e)}")

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, value):
        self._strength = self._validate_strength(value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            inverted = cv2.bitwise_not(image)
            if self._strength == 1.0:
                return inverted
            return cv2.addWeighted(image, 1 - self._strength, inverted, self._strength, 0)
        except Exception as e:
            raise RuntimeError(f"Error inverting colors: {str(e)}")

    def get_parameters(self):
        return {"strength": self._strength}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "strength" in params:
            self.strength = params["strength"]