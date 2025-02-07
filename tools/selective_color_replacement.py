# tools/selective_color_replacement.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class SelectiveColorReplacementTool(ImageProcessingTool):
    def __init__(self):
        self._target_color = [0, 0, 0]  # BGR format
        self._replacement_color = [0, 0, 0]  # BGR format
        self._tolerance = 30
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if not all(isinstance(x, (int, float)) and 0 <= x <= 255 
                      for x in self._target_color + self._replacement_color):
                raise ValueError("Color values must be between 0 and 255")
            if not isinstance(self._tolerance, (int, float)) or self._tolerance < 0 or self._tolerance > 255:
                raise ValueError("Tolerance must be between 0 and 255")
        except Exception as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def parameters(self):
        return {
            "target_color": self._target_color,
            "replacement_color": self._replacement_color,
            "tolerance": self._tolerance
        }

    @parameters.setter
    def parameters(self, values):
        if not isinstance(values, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "target_color" in values:
            self._target_color = list(values["target_color"])
        if "replacement_color" in values:
            self._replacement_color = list(values["replacement_color"])
        if "tolerance" in values:
            self._tolerance = float(values["tolerance"])
        self._validate_parameters()

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            # Create mask for target color
            lower_bound = np.array([max(0, x - self._tolerance) for x in self._target_color])
            upper_bound = np.array([min(255, x + self._tolerance) for x in self._target_color])
            mask = cv2.inRange(image, lower_bound, upper_bound)
            
            # Create replacement image
            replacement = np.full_like(image, self._replacement_color)
            
            # Combine original and replacement using mask
            result = image.copy()
            result[mask > 0] = replacement[mask > 0]
            
            return result
        except Exception as e:
            raise RuntimeError(f"Error replacing colors: {str(e)}")

    def get_parameters(self):
        return self.parameters

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        self.parameters = params