import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class ThresholdTool(ImageProcessingTool):
    def __init__(self):
        self.threshold_value = 127

    def apply(self, image):
        _, thresh = cv2.threshold(image, self.threshold_value, 255, cv2.THRESH_BINARY)
        return thresh

    def get_parameters(self):
        return {"Threshold Value": self.threshold_value}

    def update_parameters(self, params):
        if "Threshold Value" in params:
            self.threshold_value = int(params["Threshold Value"])
