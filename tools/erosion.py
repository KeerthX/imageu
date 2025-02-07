# tools/erosion.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class ErosionTool(ImageProcessingTool):
    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            kernel = np.ones((3,3), np.uint8)
            return cv2.erode(image, kernel, iterations=1)
        except Exception as e:
            raise RuntimeError(f"Error applying erosion: {str(e)}")

    def get_parameters(self):
        return {}

    def update_parameters(self, params):
        pass