import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class NoiseReductionTool(ImageProcessingTool):
    def apply(self, image):
        return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

    def get_parameters(self):
        return {}

    def update_parameters(self, params):
        pass
