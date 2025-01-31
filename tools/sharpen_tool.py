from .base_tool import ImageProcessingTool
import cv2
import numpy as np

class SharpenTool(ImageProcessingTool):
    def __init__(self):
        super().__init__()

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")

        kernel = np.array([[0, -1, 0], 
                           [-1, 5, -1], 
                           [0, -1, 0]])
        return cv2.filter2D(image, -1, kernel)

    def get_parameters(self):
        return {}

    def update_parameters(self, params):
        pass
