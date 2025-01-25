import cv2

class ContrastTool:
    def __init__(self):
        self.contrast = 1.0  # Default contrast factor

    def get_parameters(self):
        return {"contrast": self.contrast}

    def update_parameters(self, params):
        self.contrast = float(params.get("contrast", self.contrast))

    def apply(self, image):
        return cv2.convertScaleAbs(image, alpha=self.contrast, beta=0)
