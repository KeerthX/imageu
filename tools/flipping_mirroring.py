# tools/flipping_mirroring.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class FlippingMirroringTool(ImageProcessingTool):
    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            # Horizontal flip
            return cv2.flip(image, 1)
        except Exception as e:
            raise RuntimeError(f"Error flipping image: {str(e)}")

    def get_parameters(self):
        return {}

    def update_parameters(self, params):
        pass