# tools/gaussian_noise_reduction.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class GaussianNoiseReductionTool(ImageProcessingTool):
    def __init__(self):
        self._kernel_size = (5, 5)
        self._sigma_x = 0
        self._sigma_y = 0
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if not isinstance(self._kernel_size, tuple) or len(self._kernel_size) != 2:
                raise ValueError("Kernel size must be a tuple of two positive odd integers")
            if not all(isinstance(k, int) and k > 0 and k % 2 == 1 for k in self._kernel_size):
                raise ValueError("Both kernel dimensions must be positive odd integers")
            if not isinstance(self._sigma_x, (int, float)) or self._sigma_x < 0:
                raise ValueError("sigma_x must be non-negative")
            if not isinstance(self._sigma_y, (int, float)) or self._sigma_y < 0:
                raise ValueError("sigma_y must be non-negative")
        except Exception as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def parameters(self):
        return {
            "kernel_size": self._kernel_size,
            "sigma_x": self._sigma_x,
            "sigma_y": self._sigma_y
        }

    @parameters.setter
    def parameters(self, values):
        if not isinstance(values, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "kernel_size" in values:
            self._kernel_size = tuple(values["kernel_size"])
        if "sigma_x" in values:
            self._sigma_x = float(values["sigma_x"])
        if "sigma_y" in values:
            self._sigma_y = float(values["sigma_y"])
        self._validate_parameters()

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            return cv2.GaussianBlur(
                image,
                self._kernel_size,
                sigmaX=self._sigma_x,
                sigmaY=self._sigma_y
            )
        except Exception as e:
            raise RuntimeError(f"Error applying Gaussian noise reduction: {str(e)}")

    def get_parameters(self):
        return self.parameters

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        self.parameters = params

