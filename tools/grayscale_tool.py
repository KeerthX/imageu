from .base_tool import ImageProcessingTool
import cv2

class GrayscaleTool(ImageProcessingTool):
    def __init__(self):
        super().__init__()

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def get_parameters(self):
        return {}

    def update_parameters(self, params):
        pass
