import cv2

class BrightnessTool:
    def __init__(self):
        self.brightness = 1.0  # Default brightness factor

    def get_parameters(self):
        return {"brightness": self.brightness}

    def update_parameters(self, params):
        self.brightness = float(params.get("brightness", self.brightness))

    def apply(self, image):
        return cv2.convertScaleAbs(image, alpha=self.brightness, beta=0)
