# tools/vibrance_adjustment.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class VibranceAdjustmentTool(ImageProcessingTool):
    def __init__(self):
        self._vibrance = 0.0
        self._validate_vibrance(self._vibrance)

    def _validate_vibrance(self, value):
        try:
            value = float(value)
            if value < -1.0 or value > 1.0:
                raise ValueError("Vibrance must be between -1.0 and 1.0")
            return value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid vibrance value: {str(e)}")

    @property
    def vibrance(self):
        return self._vibrance

    @vibrance.setter
    def vibrance(self, value):
        self._vibrance = self._validate_vibrance(value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            # Convert to LAB color space
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB).astype(np.float32)
            # Adjust a and b channels based on vibrance
            lab[:, :, 1:] *= (1 + self._vibrance)
            lab[:, :, 1:] = np.clip(lab[:, :, 1:], 0, 255)
            return cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
        except Exception as e:
            raise RuntimeError(f"Error adjusting vibrance: {str(e)}")

    def get_parameters(self):
        return {"vibrance": self._vibrance}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "vibrance" in params:
            self.vibrance = params["vibrance"]