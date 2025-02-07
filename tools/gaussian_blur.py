# tools/gaussian_blur.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class GaussianBlurTool(ImageProcessingTool):
    def __init__(self):
        self._kernel_size = 5
        self._sigma = 1.0
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if not isinstance(self._kernel_size, int) or self._kernel_size < 1 or self._kernel_size % 2 == 0:
                raise ValueError("Kernel size must be a positive odd integer")
            if not isinstance(self._sigma, (int, float)) or self._sigma <= 0:
                raise ValueError("Sigma must be a positive number")
        except Exception as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def parameters(self):
        return {
            "kernel_size": self._kernel_size,
            "sigma": self._sigma
        }

    @parameters.setter
    def parameters(self, values):
        if not isinstance(values, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "kernel_size" in values:
            self._kernel_size = int(values["kernel_size"])
        if "sigma" in values:
            self._sigma = float(values["sigma"])
        self._validate_parameters()

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            return cv2.GaussianBlur(
                image, 
                (self._kernel_size, self._kernel_size), 
                self._sigma
            )
        except Exception as e:
            raise RuntimeError(f"Error applying Gaussian blur: {str(e)}")

    def get_parameters(self):
        return self.parameters

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        self.parameters = params