# tools/laplacian_sharpening.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class LaplacianSharpeningTool(ImageProcessingTool):
    def __init__(self):
        self._kernel_size = 3
        self._scale = 1.0
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if not isinstance(self._kernel_size, int) or self._kernel_size < 1 or self._kernel_size % 2 == 0:
                raise ValueError("Kernel size must be a positive odd integer")
            if not isinstance(self._scale, (int, float)) or self._scale <= 0:
                raise ValueError("Scale must be positive")
        except Exception as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def parameters(self):
        return {
            "kernel_size": self._kernel_size,
            "scale": self._scale
        }

    @parameters.setter
    def parameters(self, values):
        if not isinstance(values, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "kernel_size" in values:
            self._kernel_size = int(values["kernel_size"])
        if "scale" in values:
            self._scale = float(values["scale"])
        self._validate_parameters()

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            # Convert to float32 for processing
            img_float = image.astype(np.float32)
            # Apply Laplacian
            laplacian = cv2.Laplacian(img_float, cv2.CV_32F, ksize=self._kernel_size)
            # Apply sharpening
            sharpened = img_float + self._scale * laplacian
            # Clip values and convert back to uint8
            return np.clip(sharpened, 0, 255).astype(np.uint8)
        except Exception as e:
            raise RuntimeError(f"Error applying Laplacian sharpening: {str(e)}")

    def get_parameters(self):
        return self.parameters

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        self.parameters = params