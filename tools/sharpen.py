import cv2
import numpy as np

class SharpenTool:
    def __init__(self):
        self.amount = 1.0  # Default sharpening factor

    def get_parameters(self):
        return {"amount": self.amount}

    def update_parameters(self, params):
        self.amount = float(params.get("amount", self.amount))

    def apply(self, image):
        kernel = np.array([[0, -1, 0], [-1, 5 * self.amount, -1], [0, -1, 0]])
        return cv2.filter2D(image, -1, kernel)
