# tools/gabor_filter.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class GaborFilterTool(ImageProcessingTool):
    def __init__(self):
        self._kernel_size = 31
        self._sigma = 4.0
        self._theta = 0.0
        self._lambda = 10.0
        self._gamma = 0.5
        self._psi = 0.0
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if self._kernel_size <= 0 or self._kernel_size % 2 == 0:
                raise ValueError("Kernel size must be an odd positive number")
            if self._sigma <= 0:
                raise ValueError("Sigma must be positive")
            if self._lambda <= 0:
                raise ValueError("Lambda must be positive")
            if self._gamma <= 0:
                raise ValueError("Gamma must be positive")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        
        try:
            kernel = cv2.getGaborKernel(
                (self._kernel_size, self._kernel_size),
                self._sigma,
                self._theta,
                self._lambda,
                self._gamma,
                self._psi
            )
            return cv2.filter2D(image, cv2.CV_8UC3, kernel)
        except Exception as e:
            raise RuntimeError(f"Error applying Gabor filter: {str(e)}")

    def get_parameters(self):
        return {
            "kernel_size": self._kernel_size,
            "sigma": self._sigma,
            "theta": self._theta,
            "lambda": self._lambda,
            "gamma": self._gamma,
            "psi": self._psi
        }

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "kernel_size" in params:
            self._kernel_size = int(params["kernel_size"])
        if "sigma" in params:
            self._sigma = float(params["sigma"])
        if "theta" in params:
            self._theta = float(params["theta"])
        if "lambda" in params:
            self._lambda = float(params["lambda"])
        if "gamma" in params:
            self._gamma = float(params["gamma"])
        if "psi" in params:
            self._psi = float(params["psi"])
        
        self._validate_parameters()