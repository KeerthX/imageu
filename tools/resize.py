import cv2


class ResizeTool:
    def __init__(self):
        self.width = 100
        self.height = 100

    def apply(self, image):
        return cv2.resize(image, (self.width, self.height))

    def get_parameters(self):
        return {"width": self.width, "height": self.height}
