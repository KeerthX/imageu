# tools/laplacian_edge_detection.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class LaplacianEdgeDetectionTool(ImageProcessingTool):
    def __init__(self):
        self._kernel_size = 3
        self._scale = 1.0
        self._delta = 0
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if not isinstance(self._kernel_size, int) or self._kernel_size < 1 or self._kernel_size % 2 == 0:
                raise ValueError("Kernel size must be a positive odd integer")
            if not isinstance(self._scale, (int, float)) or self._scale <= 0:
                raise ValueError("Scale must be positive")
            if not isinstance(self._delta, (int, float)):
                raise ValueError("Delta must be a number")
        except Exception as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def parameters(self):
        return {
            "kernel_size": self._kernel_size,
            "scale": self._scale,
            "delta": self._delta
        }

    @parameters.setter
    def parameters(self, values):
        if not isinstance(values, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "kernel_size" in values:
            self._kernel_size = int(values["kernel_size"])
        if "scale" in values:
            self._scale = float(values["scale"])
        if "delta" in values:
            self._delta = float(values["delta"])
        self._validate_parameters()

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()

            edges = cv2.Laplacian(
                gray,
                cv2.CV_64F,
                ksize=self._kernel_size,
                scale=self._scale,
                delta=self._delta
            )
            
            # Convert back to uint8
            abs_edges = np.absolute(edges)
            return np.uint8(abs_edges)
        except Exception as e:
            raise RuntimeError(f"Error applying Laplacian edge detection: {str(e)}")

    def get_parameters(self):
        return self.parameters

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        self.parameters = params

