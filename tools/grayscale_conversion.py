# tools/grayscale_conversion.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class GrayscaleConversionTool(ImageProcessingTool):
    def __init__(self):
        self._weights = [0.299, 0.587, 0.114]  # Standard BT.601 weights
        self._validate_weights(self._weights)

    def _validate_weights(self, weights):
        try:
            if len(weights) != 3:
                raise ValueError("Must provide exactly 3 weights for RGB channels")
            weights = [float(w) for w in weights]
            if not np.isclose(sum(weights), 1.0):
                raise ValueError("Weights must sum to 1.0")
            return weights
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid weights: {str(e)}")

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, values):
        self._weights = self._validate_weights(values)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            raise RuntimeError(f"Error converting to grayscale: {str(e)}")

    def get_parameters(self):
        return {"weights": self._weights}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "weights" in params:
            self.weights = params["weights"]
