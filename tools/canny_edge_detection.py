# tools/canny_edge_detection.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class CannyEdgeDetectionTool(ImageProcessingTool):
    def __init__(self):
        self._threshold1 = 100
        self._threshold2 = 200
        self._aperture_size = 3
        self._l2gradient = False
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if not isinstance(self._threshold1, (int, float)) or self._threshold1 < 0:
                raise ValueError("Threshold1 must be non-negative")
            if not isinstance(self._threshold2, (int, float)) or self._threshold2 < 0:
                raise ValueError("Threshold2 must be non-negative")
            if not isinstance(self._aperture_size, int) or self._aperture_size not in [3, 5, 7]:
                raise ValueError("Aperture size must be 3, 5, or 7")
            if not isinstance(self._l2gradient, bool):
                raise ValueError("L2gradient must be boolean")
        except Exception as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def parameters(self):
        return {
            "threshold1": self._threshold1,
            "threshold2": self._threshold2,
            "aperture_size": self._aperture_size,
            "l2gradient": self._l2gradient
        }

    @parameters.setter
    def parameters(self, values):
        if not isinstance(values, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "threshold1" in values:
            self._threshold1 = float(values["threshold1"])
        if "threshold2" in values:
            self._threshold2 = float(values["threshold2"])
        if "aperture_size" in values:
            self._aperture_size = int(values["aperture_size"])
        if "l2gradient" in values:
            self._l2gradient = bool(values["l2gradient"])
        self._validate_parameters()

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
                
            edges = cv2.Canny(
                gray,
                self._threshold1,
                self._threshold2,
                apertureSize=self._aperture_size,
                L2gradient=self._l2gradient
            )
            return edges
        except Exception as e:
            raise RuntimeError(f"Error applying Canny edge detection: {str(e)}")

    def get_parameters(self):
        return self.parameters

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        self.parameters = params