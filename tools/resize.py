import cv2

class ResizeTool:
    def __init__(self):
        self.width = 100
        self.height = 100

    def configure(self):
        print("Configure Resize: (Example: width=100, height=100)")

    def apply(self, image):
        return cv2.resize(image, (self.width, self.height))
