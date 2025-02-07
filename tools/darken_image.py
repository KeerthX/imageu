# tools/darken_image.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class DarkenImageTool(ImageProcessingTool):
    def __init__(self):
        self._amount = 0.2
        self._validate_amount(self._amount)

    def _validate_amount(self, value):
        try:
            value = float(value)
            if value < 0.0 or value > 1.0:
                raise ValueError("Darkening amount must be between 0.0 and 1.0")
            return value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid darkening amount: {str(e)}")

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = self._validate_amount(value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            return cv2.multiply(image, np.array([1.0 - self._amount])).astype(np.uint8)
        except Exception as e:
            raise RuntimeError(f"Error darkening image: {str(e)}")

    def get_parameters(self):
        return {"amount": self._amount}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "amount" in params:
            self.amount = params["amount"]
