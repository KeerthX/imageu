# tools/high_pass_filter.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class HighPassFilterTool(ImageProcessingTool):
    def __init__(self):
        self._kernel_size = 3
        self._sigma = 1.0
        self._validate_parameters(self._kernel_size, self._sigma)

    def _validate_parameters(self, kernel_size, sigma):
        try:
            kernel_size = int(kernel_size)
            sigma = float(sigma)
            
            if kernel_size <= 0 or kernel_size % 2 == 0:
                raise ValueError("Kernel size must be an odd positive number")
            if sigma <= 0:
                raise ValueError("Sigma must be a positive number")
                
            return kernel_size, sigma
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def kernel_size(self):
        return self._kernel_size

    @kernel_size.setter
    def kernel_size(self, value):
        self._kernel_size, _ = self._validate_parameters(value, self._sigma)

    @property
    def sigma(self):
        return self._sigma

    @sigma.setter
    def sigma(self, value):
        _, self._sigma = self._validate_parameters(self._kernel_size, value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
            
        try:
            # Create low pass filter
            blur = cv2.GaussianBlur(image, (self._kernel_size, self._kernel_size), self._sigma)
            # Subtract from original image to get high pass
            return cv2.subtract(image, blur)
        except Exception as e:
            raise RuntimeError(f"Error applying high pass filter: {str(e)}")

    def get_parameters(self):
        return {
            "kernel_size": self._kernel_size,
            "sigma": self._sigma
        }

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "kernel_size" in params:
            self.kernel_size = params["kernel_size"]
        if "sigma" in params:
            self.sigma = params["sigma"]