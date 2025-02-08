# tools/lbp.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class LBPTool(ImageProcessingTool):
    def __init__(self):
        self._radius = 1
        self._n_points = 8
        self._method = 'uniform'
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if self._radius <= 0:
                raise ValueError("Radius must be positive")
            if self._n_points <= 0:
                raise ValueError("Number of points must be positive")
            if self._method not in ['default', 'uniform', 'ror', 'nri_uniform']:
                raise ValueError("Invalid method. Must be one of: default, uniform, ror, nri_uniform")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    def _calculate_lbp(self, image, radius, n_points):
        height, width = image.shape
        lbp = np.zeros((height, width), dtype=np.uint8)
        for h in range(radius, height-radius):
            for w in range(radius, width-radius):
                center = image[h, w]
                binary = ""
                for p in range(n_points):
                    angle = 2 * np.pi * p / n_points
                    x = w + radius * np.cos(angle)
                    y = h - radius * np.sin(angle)
                    x1 = int(np.floor(x))
                    y1 = int(np.floor(y))
                    binary += "1" if image[y1, x1] >= center else "0"
                lbp[h, w] = int(binary, 2)
        return lbp

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        
        try:
            if len(image.shape) > 2:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return self._calculate_lbp(image, self._radius, self._n_points)
        except Exception as e:
            raise RuntimeError(f"Error applying LBP: {str(e)}")

    def get_parameters(self):
        return {
            "radius": self._radius,
            "n_points": self._n_points,
            "method": self._method
        }

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "radius" in params:
            self._radius = int(params["radius"])
        if "n_points" in params:
            self._n_points = int(params["n_points"])
        if "method" in params:
            self._method = str(params["method"])
        
        self._validate_parameters()