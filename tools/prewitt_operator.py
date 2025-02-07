# tools/prewitt_operator.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class PrewittOperatorTool(ImageProcessingTool):
    def __init__(self):
        self._direction = 'both'  # 'x', 'y', or 'both'
        self._scale = 1.0
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if self._direction not in ['x', 'y', 'both']:
                raise ValueError("Direction must be 'x', 'y', or 'both'")
            if not isinstance(self._scale, (int, float)) or self._scale <= 0:
                raise ValueError("Scale must be positive")
        except Exception as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def parameters(self):
        return {
            "direction": self._direction,
            "scale": self._scale
        }

    @parameters.setter
    def parameters(self, values):
        if not isinstance(values, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "direction" in values:
            self._direction = str(values["direction"]).lower()
        if "scale" in values:
            self._scale = float(values["scale"])
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

            # Define Prewitt kernels
            kernelx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
            kernely = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])

            if self._direction == 'x':
                gradient = cv2.filter2D(gray, -1, kernelx * self._scale)
            elif self._direction == 'y':
                gradient = cv2.filter2D(gray, -1, kernely * self._scale)
            else:  # both
                grad_x = cv2.filter2D(gray, -1, kernelx * self._scale)
                grad_y = cv2.filter2D(gray, -1, kernely * self._scale)
                gradient = np.sqrt(grad_x**2 + grad_y**2)

            return np.clip(gradient, 0, 255).astype(np.uint8)
        except Exception as e:
            raise RuntimeError(f"Error applying Prewitt operator: {str(e)}")

    def get_parameters(self):
        return self.parameters

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        self.parameters = params