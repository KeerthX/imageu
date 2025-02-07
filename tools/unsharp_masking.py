# tools/unsharp_masking.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class UnsharpMaskingTool(ImageProcessingTool):
    def __init__(self):
        self._kernel_size = 5
        self._amount = 1.5
        self._threshold = 0
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if not isinstance(self._kernel_size, int) or self._kernel_size < 1 or self._kernel_size % 2 == 0:
                raise ValueError("Kernel size must be a positive odd integer")
            if not isinstance(self._amount, (int, float)) or self._amount < 0:
                raise ValueError("Amount must be non-negative")
            if not isinstance(self._threshold, (int, float)) or self._threshold < 0:
                raise ValueError("Threshold must be non-negative")
        except Exception as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def parameters(self):
        return {
            "kernel_size": self._kernel_size,
            "amount": self._amount,
            "threshold": self._threshold
        }

    @parameters.setter
    def parameters(self, values):
        if not isinstance(values, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "kernel_size" in values:
            self._kernel_size = int(values["kernel_size"])
        if "amount" in values:
            self._amount = float(values["amount"])
        if "threshold" in values:
            self._threshold = float(values["threshold"])
        self._validate_parameters()

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            # Create the Gaussian blur
            gaussian = cv2.GaussianBlur(image, (self._kernel_size, self._kernel_size), 0)
            # Calculate the unsharp mask
            unsharp_mask = cv2.addWeighted(image, 1.0 + self._amount, gaussian, -self._amount, 0)
            # Apply threshold if specified
            if self._threshold > 0:
                diff = cv2.absdiff(unsharp_mask, image)
                mask = diff > self._threshold
                unsharp_mask[~mask] = image[~mask]
            return unsharp_mask
        except Exception as e:
            raise RuntimeError(f"Error applying unsharp mask: {str(e)}")

    def get_parameters(self):
        return self.parameters

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        self.parameters = params