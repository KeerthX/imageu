# tools/sepia_effect.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class SepiaEffectTool(ImageProcessingTool):
    def __init__(self):
        self._intensity = 1.0
        self._validate_intensity(self._intensity)

    def _validate_intensity(self, value):
        try:
            value = float(value)
            if value < 0.0 or value > 1.0:
                raise ValueError("Sepia intensity must be between 0.0 and 1.0")
            return value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid intensity value: {str(e)}")

    @property
    def intensity(self):
        return self._intensity

    @intensity.setter
    def intensity(self, value):
        self._intensity = self._validate_intensity(value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            # Sepia matrix
            sepia_matrix = np.array([
                [0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]
            ])
            
            sepia = cv2.transform(image, sepia_matrix)
            sepia = np.clip(sepia, 0, 255).astype(np.uint8)
            
            # Blend with original based on intensity
            return cv2.addWeighted(image, 1 - self._intensity, sepia, self._intensity, 0)
        except Exception as e:
            raise RuntimeError(f"Error applying sepia effect: {str(e)}")

    def get_parameters(self):
        return {"intensity": self._intensity}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "intensity" in params:
            self.intensity = params["intensity"]
