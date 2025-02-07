# tools/bilateral_filter.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class BilateralFilterTool(ImageProcessingTool):
    def __init__(self):
        self._d = 9
        self._sigma_color = 75
        self._sigma_space = 75
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if not isinstance(self._d, int) or self._d < 1:
                raise ValueError("Diameter must be a positive integer")
            if not isinstance(self._sigma_color, (int, float)) or self._sigma_color <= 0:
                raise ValueError("Color sigma must be positive")
            if not isinstance(self._sigma_space, (int, float)) or self._sigma_space <= 0:
                raise ValueError("Space sigma must be positive")
        except Exception as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def parameters(self):
        return {
            "d": self._d,
            "sigma_color": self._sigma_color,
            "sigma_space": self._sigma_space
        }

    @parameters.setter
    def parameters(self, values):
        if not isinstance(values, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "d" in values:
            self._d = int(values["d"])
        if "sigma_color" in values:
            self._sigma_color = float(values["sigma_color"])
        if "sigma_space" in values:
            self._sigma_space = float(values["sigma_space"])
        self._validate_parameters()

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            return cv2.bilateralFilter(
                image,
                self._d,
                self._sigma_color,
                self._sigma_space
            )
        except Exception as e:
            raise RuntimeError(f"Error applying bilateral filter: {str(e)}")

    def get_parameters(self):
        return self.parameters

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        self.parameters = params
