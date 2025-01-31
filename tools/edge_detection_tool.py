from .base_tool import ImageProcessingTool
import cv2

class EdgeDetectionTool(ImageProcessingTool):
    def __init__(self):
        super().__init__()
        self.threshold1 = 100
        self.threshold2 = 200

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        
        return cv2.Canny(image, self.threshold1, self.threshold2)

    def get_parameters(self):
        return {"Threshold1": self.threshold1, "Threshold2": self.threshold2}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "Threshold1" in params:
            self.threshold1 = params["Threshold1"]
        if "Threshold2" in params:
            self.threshold2 = params["Threshold2"]
