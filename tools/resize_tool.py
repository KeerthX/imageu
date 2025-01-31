from .base_tool import ImageProcessingTool
import cv2

class ResizeTool(ImageProcessingTool):
    def __init__(self):
        super().__init__()
        self.width = 100
        self.height = 100

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        
        return cv2.resize(image, (self.width, self.height), interpolation=cv2.INTER_AREA)

    def get_parameters(self):
        return {"Width": self.width, "Height": self.height}

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")

        if "Width" in params:
            self.width = params["Width"]
        if "Height" in params:
            self.height = params["Height"]
