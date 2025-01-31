from .base_tool import ImageProcessingTool
import cv2
import numpy as np

class ContrastTool(ImageProcessingTool):
    def __init__(self):
        super().__init__()
        self.contrast = 1.0  # Default contrast level

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        
        return cv2.convertScaleAbs(image, alpha=self.contrast, beta=0)

    def get_parameters(self):
        return {"Contrast": self.contrast}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")

        if "Contrast" in params:
            if not isinstance(params["Contrast"], (int, float)):
                raise ValueError("Contrast must be an integer or float")
            self.contrast = params["Contrast"]
