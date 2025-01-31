import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class HistogramEqualizationTool(ImageProcessingTool):
    def apply(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.equalizeHist(gray)

    def get_parameters(self):
        return {}

    def update_parameters(self, params):
        pass
