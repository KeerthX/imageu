import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class SepiaTool(ImageProcessingTool):
    def apply(self, image):
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        return cv2.transform(image, kernel)

    def get_parameters(self):
        return {}

    def update_parameters(self, params):
        pass
