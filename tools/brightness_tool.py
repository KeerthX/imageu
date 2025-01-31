from .base_tool import ImageProcessingTool
import cv2
import numpy as np

class BrightnessTool(ImageProcessingTool):
    def __init__(self):
        super().__init__()
        self.brightness = 0  # Default brightness level

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        
        brightness = np.full_like(image, self.brightness, dtype=image.dtype)
        return cv2.add(image, brightness)

    def get_parameters(self):
        return {"Brightness": self.brightness}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "Brightness" in params:
            if not isinstance(params["Brightness"], (int, float)):
                raise ValueError("Brightness must be an integer or float")
            self.brightness = params["Brightness"]
