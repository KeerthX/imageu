import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class FlipTool(ImageProcessingTool):
    def __init__(self):
        self.axis = 0  # 0: Vertical, 1: Horizontal, -1: Both

    def apply(self, image):
        return cv2.flip(image, self.axis)

    def get_parameters(self):
        return {"Axis": self.axis}

    def update_parameters(self, params):
        if "Axis" in params:
            self.axis = int(params["Axis"])
