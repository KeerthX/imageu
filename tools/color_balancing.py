# tools/color_balancing.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class ColorBalancingTool(ImageProcessingTool):
    def __init__(self):
        self._red_balance = 1.0
        self._green_balance = 1.0
        self._blue_balance = 1.0
        self._validate_balance_values()

    def _validate_balance_values(self):
        try:
            for value in [self._red_balance, self._green_balance, self._blue_balance]:
                if not isinstance(value, (int, float)):
                    raise ValueError("Balance values must be numbers")
                if value < 0.0 or value > 2.0:
                    raise ValueError("Balance values must be between 0.0 and 2.0")
        except Exception as e:
            raise ValueError(f"Invalid balance values: {str(e)}")

    @property
    def balance_values(self):
        return {
            "red": self._red_balance,
            "green": self._green_balance,
            "blue": self._blue_balance
        }

    @balance_values.setter
    def balance_values(self, values):
        if not isinstance(values, dict):
            raise ValueError("Balance values must be provided as a dictionary")
        if "red" in values:
            self._red_balance = float(values["red"])
        if "green" in values:
            self._green_balance = float(values["green"])
        if "blue" in values:
            self._blue_balance = float(values["blue"])
        self._validate_balance_values()

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            # Split the channels
            b, g, r = cv2.split(image)
            
            # Apply balance to each channel
            r = cv2.multiply(r, self._red_balance)
            g = cv2.multiply(g, self._green_balance)
            b = cv2.multiply(b, self._blue_balance)
            
            # Clip values and merge
            balanced = cv2.merge([
                np.clip(b, 0, 255).astype(np.uint8),
                np.clip(g, 0, 255).astype(np.uint8),
                np.clip(r, 0, 255).astype(np.uint8)
            ])
            return balanced
        except Exception as e:
            raise RuntimeError(f"Error balancing colors: {str(e)}")

    def get_parameters(self):
        return self.balance_values

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        self.balance_values = params